#!/usr/bin/env python3
"""
github-sync — Safe Git sync for any shared repository.

Core principle: ALWAYS stage before any destructive git operation.
Staged files are recoverable via git reflog; untracked files are not.

Per-repo behavior is controlled by an optional `.sync.toml` at the repo
root. With no config, the script is strict-safe: every conflict goes
to manual review.
"""

import argparse
import fnmatch
import os
import re
import socket
import subprocess
import sys
import tomllib
from datetime import datetime
from pathlib import Path


# ---------- config ----------

DEFAULT_CONFIG = {
    "default_strategy": "manual",
    "never_touch": [],
    "merge_rules": [],
}


def load_config(repo_path: Path) -> dict:
    config_path = repo_path / ".sync.toml"
    if not config_path.exists():
        return dict(DEFAULT_CONFIG)
    with open(config_path, "rb") as f:
        loaded = tomllib.load(f)
    cfg = dict(DEFAULT_CONFIG)
    cfg.update(loaded)
    cfg.setdefault("merge_rules", [])
    cfg.setdefault("never_touch", [])
    cfg.setdefault("default_strategy", "manual")
    return cfg


def _glob_match(filepath: str, pattern: str) -> bool:
    if "**" in pattern:
        regex = re.escape(pattern).replace(r"\*\*", ".*").replace(r"\*", "[^/]*").replace(r"\?", ".")
        return bool(re.fullmatch(regex, filepath))
    return fnmatch.fnmatch(filepath, pattern)


def matches_any(filepath: str, patterns: list[str]) -> bool:
    return any(_glob_match(filepath, p) for p in patterns)


def strategy_for(filepath: str, config: dict) -> str:
    if matches_any(filepath, config["never_touch"]):
        return "never_touch"
    for rule in config["merge_rules"]:
        if _glob_match(filepath, rule["match"]):
            return rule["strategy"]
    return config["default_strategy"]


# ---------- git plumbing ----------

def run_git(args: list[str], cwd: Path, capture: bool = True, check: bool = True) -> subprocess.CompletedProcess:
    cmd = ["git"] + args
    return subprocess.run(cmd, cwd=cwd, capture_output=capture, text=True, check=check)


def repo_toplevel(path: Path) -> Path | None:
    try:
        result = run_git(["rev-parse", "--show-toplevel"], cwd=path)
        return Path(result.stdout.strip())
    except subprocess.CalledProcessError:
        return None


# ---------- logging ----------

def log_sync(repo_path: Path, message: str, verbose: bool = False):
    log_file = repo_path / ".sync_log"
    timestamp = datetime.now().isoformat()
    hostname = socket.gethostname()
    workspace = str(repo_path.resolve())
    entry = f"[{timestamp}] [{hostname}:{workspace}] {message}\n"
    with open(log_file, "a") as f:
        f.write(entry)
    if verbose:
        print(f"  {message}")


def get_workspace_info(repo_path: Path) -> dict:
    return {
        "hostname": socket.gethostname(),
        "path": str(repo_path.resolve()),
        "timestamp": datetime.now().isoformat(),
        "user": os.environ.get("USER", "unknown"),
    }


# ---------- environment hygiene ----------

def ensure_gitignore(repo_path: Path, dry_run: bool, verbose: bool) -> bool:
    gitignore_path = repo_path / ".gitignore"
    default_template = Path(__file__).resolve().parent.parent / "resources" / "default_gitignore.txt"

    if gitignore_path.exists():
        content = gitignore_path.read_text()
        if ".sync_log" not in content:
            if not dry_run:
                with open(gitignore_path, "a") as f:
                    f.write("\n# Local sync log (workspace-specific)\n.sync_log\n")
                log_sync(repo_path, "Added .sync_log to existing .gitignore", verbose)
            else:
                log_sync(repo_path, "[DRY RUN] Would add .sync_log to .gitignore", verbose)
            return True
        log_sync(repo_path, ".gitignore already covers .sync_log", verbose)
        return False

    if dry_run:
        log_sync(repo_path, "[DRY RUN] Would create .gitignore", verbose)
        return True

    if default_template.exists():
        content = default_template.read_text()
    else:
        content = "# Sync log (local only)\n.sync_log\n"
    gitignore_path.write_text(content)
    log_sync(repo_path, "Created .gitignore with standard exclusions", verbose)
    return True


def clean_cached_python_files(repo_path: Path, dry_run: bool, verbose: bool) -> int:
    pyc = run_git(["ls-files", "*.pyc", "**/*.pyc"], cwd=repo_path, check=False).stdout.strip().split("\n")
    cache = run_git(["ls-files", "**/__pycache__/*"], cwd=repo_path, check=False).stdout.strip().split("\n")
    cached = [f for f in pyc + cache if f]
    if not cached:
        log_sync(repo_path, "No cached Python files in git index", verbose)
        return 0
    if dry_run:
        log_sync(repo_path, f"[DRY RUN] Would remove {len(cached)} cached files from index", verbose)
        return len(cached)
    for f in cached:
        run_git(["rm", "--cached", "-f", f], cwd=repo_path, check=False)
    log_sync(repo_path, f"Removed {len(cached)} cached Python files from git index", verbose)
    return len(cached)


# ---------- safety net ----------

def get_untracked_files(repo_path: Path) -> list[str]:
    result = run_git(["status", "--porcelain"], cwd=repo_path)
    return [line[3:] for line in result.stdout.strip().split("\n") if line.startswith("??")]


def safety_stage_all(repo_path: Path, dry_run: bool, verbose: bool) -> int:
    """
    THE CRITICAL SAFETY NET: stage everything before any destructive operation.

    Staged files live in git's object database and are recoverable via reflog.
    Untracked files exist only on disk and can be lost forever.
    """
    if dry_run:
        untracked = get_untracked_files(repo_path)
        log_sync(repo_path, f"[DRY RUN] Would stage all files ({len(untracked)} untracked)", verbose)
        return len(untracked)

    run_git(["add", "."], cwd=repo_path)
    result = run_git(["diff", "--cached", "--name-only"], cwd=repo_path, check=False)
    staged = [f for f in result.stdout.strip().split("\n") if f]

    if staged:
        log_sync(repo_path, f"SAFETY NET: Staged {len(staged)} files", verbose)
        if verbose:
            print("    Staged files:")
            for f in staged[:10]:
                print(f"      - {f}")
            if len(staged) > 10:
                print(f"      ... and {len(staged) - 10} more")
        return len(staged)
    log_sync(repo_path, "No changes to stage", verbose)
    return 0


# ---------- conflict resolution ----------

CONFLICT_RE = re.compile(r"<<<<<<< HEAD\n(.*?)\n=======\n(.*?)\n>>>>>>> [^\n]+", re.DOTALL)


def archive_discarded(repo_path: Path, filepath: str, content: str, source: str, verbose: bool):
    archive_dir = repo_path / ".conflict_archive"
    archive_dir.mkdir(exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    safe = filepath.replace("/", "_").replace("\\", "_")
    out = archive_dir / f"{timestamp}_{source}_{safe}"
    out.write_text(content)
    log_sync(repo_path, f"Archived discarded {source} version → {out.name}", verbose)


def extract_versions(content: str) -> tuple[str, str] | None:
    m = CONFLICT_RE.search(content)
    return (m.group(1), m.group(2)) if m else None


def strategy_combine_unique_lines(repo_path: Path, full_path: Path, verbose: bool) -> bool:
    """Append-only files: keep all unique lines from both sides."""
    content = full_path.read_text()
    versions = extract_versions(content)
    if not versions:
        return False
    ours, theirs = versions
    seen = {}
    for line in ours.split("\n") + theirs.split("\n"):
        seen.setdefault(line, True)
    combined = "\n".join(seen.keys())
    resolved = CONFLICT_RE.sub(combined, content)
    full_path.write_text(resolved)
    run_git(["add", str(full_path.relative_to(repo_path))], cwd=repo_path)
    log_sync(repo_path, f"Combined both versions of {full_path.name} ({len(seen)} unique lines)", verbose)
    return True


def strategy_longer_wins(repo_path: Path, full_path: Path, verbose: bool) -> bool:
    """Take the longer side; archive the shorter."""
    content = full_path.read_text()
    versions = extract_versions(content)
    if not versions:
        return False
    ours, theirs = versions
    if len(ours) >= len(theirs):
        winner, loser, loser_src = ours, theirs, "theirs"
    else:
        winner, loser, loser_src = theirs, ours, "ours"
    rel = str(full_path.relative_to(repo_path))
    archive_discarded(repo_path, rel, loser, loser_src, verbose)
    resolved = CONFLICT_RE.sub(winner, content)
    full_path.write_text(resolved)
    run_git(["add", rel], cwd=repo_path)
    log_sync(repo_path, f"Kept longer version of {full_path.name} ({len(winner)} vs {len(loser)} chars)", verbose)
    return True


def parse_skills_table(content: str) -> list[dict]:
    skills = []
    in_table = False
    for line in content.split("\n"):
        if re.match(r"^\|[-\s|]+\|$", line):
            in_table = True
            continue
        if in_table and line.startswith("|") and line.endswith("|"):
            parts = [p.strip() for p in line.split("|")[1:-1]]
            if len(parts) >= 3:
                skills.append({"skill": parts[0], "description": parts[1], "status": parts[2]})
    return skills


def strategy_table_merge_skills_readme(repo_path: Path, full_path: Path, verbose: bool) -> bool:
    """Skills-specific README merge: union the skills table, sort alphabetically."""
    content = full_path.read_text()
    if "<<<<<<< HEAD" not in content:
        return False

    ours_match = re.search(r"<<<<<<< HEAD\n(.*?)\n=======", content, re.DOTALL)
    theirs_match = re.search(r"=======\n(.*?)\n>>>>>>> ", content, re.DOTALL)
    if not ours_match or not theirs_match:
        return False

    ours_skills = parse_skills_table(ours_match.group(1))
    theirs_skills = parse_skills_table(theirs_match.group(1))

    merged = {}
    for s in ours_skills + theirs_skills:
        existing = merged.get(s["skill"])
        if existing is None or len(s["description"]) > len(existing["description"]):
            merged[s["skill"]] = s

    sorted_skills = sorted(merged.values(), key=lambda x: x["skill"].lower())
    table_lines = ["| Skill | Description | Status |", "|-------|-------------|--------|"]
    for s in sorted_skills:
        table_lines.append(f"| {s['skill']} | {s['description']} | {s['status']} |")
    new_table = "\n".join(table_lines)

    original = run_git(["show", "HEAD:README.md"], cwd=repo_path, check=False).stdout
    if not original:
        return False
    table_start = original.find("| Skill |")
    if table_start < 0:
        return False
    table_end = original.rfind("| Active |") + len("| Active |")
    after = original[table_end:].lstrip("\n")
    rebuilt = original[:table_start] + new_table + "\n\n" + after
    full_path.write_text(rebuilt)
    run_git(["add", "README.md"], cwd=repo_path)
    log_sync(repo_path, f"Auto-resolved README.md (merged {len(sorted_skills)} skills)", verbose)
    return True


STRATEGY_DISPATCH = {
    "combine_unique_lines": strategy_combine_unique_lines,
    "longer_wins": strategy_longer_wins,
    "table_merge_skills_readme": strategy_table_merge_skills_readme,
}


def get_conflicted_files(repo_path: Path) -> list[str]:
    result = run_git(["diff", "--name-only", "--diff-filter=U"], cwd=repo_path, check=False)
    return [f for f in result.stdout.strip().split("\n") if f]


def resolve_one(repo_path: Path, filepath: str, config: dict, verbose: bool) -> tuple[bool, str]:
    full = repo_path / filepath
    if not full.exists():
        return False, "file_not_found"

    strategy = strategy_for(filepath, config)

    if strategy in ("manual", "never_touch"):
        log_sync(repo_path, f"MANUAL REQUIRED: {filepath} ({strategy})", verbose)
        return False, strategy

    fn = STRATEGY_DISPATCH.get(strategy)
    if fn is None:
        log_sync(repo_path, f"MANUAL REQUIRED: {filepath} (unknown strategy '{strategy}')", verbose)
        return False, f"unknown_strategy:{strategy}"

    if fn(repo_path, full, verbose):
        return True, strategy
    return False, f"{strategy}_failed"


def resolve_all(repo_path: Path, config: dict, verbose: bool) -> tuple[int, list[str]]:
    conflicted = get_conflicted_files(repo_path)
    if not conflicted:
        return 0, []
    resolved = 0
    manual_files = []
    for f in conflicted:
        ok, strategy = resolve_one(repo_path, f, config, verbose)
        if ok:
            resolved += 1
            if verbose:
                print(f"    Resolved {f} ({strategy})")
        else:
            manual_files.append(f)
            if verbose:
                print(f"    MANUAL: {f} ({strategy})")
    return resolved, manual_files


# ---------- pull / push ----------

def pull_rebase(repo_path: Path, remote: str, branch: str, config: dict, dry_run: bool, verbose: bool) -> tuple[bool, str]:
    if dry_run:
        log_sync(repo_path, f"[DRY RUN] Would: git pull --rebase {remote} {branch}", verbose)
        return True, "dry run"

    log_sync(repo_path, f"Pulling --rebase from {remote}/{branch}…", verbose)
    result = run_git(["pull", "--rebase", remote, branch], cwd=repo_path, check=False)
    if result.returncode == 0:
        log_sync(repo_path, "Pull successful", verbose)
        return True, "success"

    if "CONFLICT" in result.stdout or "CONFLICT" in result.stderr:
        log_sync(repo_path, "Conflicts detected, attempting config-driven resolution…", verbose)
        resolved, manual_files = resolve_all(repo_path, config, verbose)

        if not manual_files:
            env = os.environ.copy()
            env["GIT_EDITOR"] = "true"
            cont = subprocess.run(
                ["git", "rebase", "--continue"],
                cwd=repo_path, capture_output=True, text=True, check=False, env=env,
            )
            if cont.returncode == 0:
                log_sync(repo_path, f"Rebase continued after auto-resolving {resolved} conflicts", verbose)
                return True, f"resolved_{resolved}_conflicts"
            if "CONFLICT" in cont.stdout or "CONFLICT" in cont.stderr:
                # Multi-commit rebase — recurse into the next batch.
                return pull_rebase(repo_path, remote, branch, config, dry_run, verbose)

        if manual_files:
            log_sync(repo_path, f"AUTO-RESOLVED: {resolved} files", verbose)
            log_sync(repo_path, f"MANUAL REQUIRED: {len(manual_files)} files: {', '.join(manual_files)}", verbose)
            run_git(["rebase", "--abort"], cwd=repo_path, check=False)
            return False, f"manual_required:{','.join(manual_files)}"

        run_git(["rebase", "--abort"], cwd=repo_path, check=False)
        log_sync(repo_path, "REBASE ABORTED: conflicts require manual resolution", verbose)
        return False, "conflict"

    run_git(["rebase", "--abort"], cwd=repo_path, check=False)
    err = result.stderr or result.stdout or "Unknown error"
    log_sync(repo_path, f"REBASE ABORTED: {err}", verbose)
    return False, err


def push(repo_path: Path, remote: str, branch: str, dry_run: bool, verbose: bool) -> tuple[bool, str]:
    if dry_run:
        log_sync(repo_path, f"[DRY RUN] Would: git push {remote} {branch}", verbose)
        return True, "dry run"
    log_sync(repo_path, f"Pushing to {remote}/{branch}…", verbose)
    result = run_git(["push", remote, branch], cwd=repo_path, check=False)
    if result.returncode == 0:
        log_sync(repo_path, "Push successful", verbose)
        return True, "success"
    if "rejected" in result.stderr and ("non-fast-forward" in result.stderr or "fetch first" in result.stderr):
        log_sync(repo_path, "PUSH REJECTED: remote has new changes. Run sync again.", verbose)
        return False, "needs_pull"
    err = result.stderr or result.stdout or "Unknown error"
    log_sync(repo_path, f"PUSH FAILED: {err}", verbose)
    return False, err


def commit_if_needed(repo_path: Path, dry_run: bool, verbose: bool) -> bool:
    result = run_git(["diff", "--cached", "--quiet"], cwd=repo_path, check=False)
    if result.returncode == 0:
        return False
    if dry_run:
        log_sync(repo_path, "[DRY RUN] Would commit staged changes", verbose)
        return True
    info = get_workspace_info(repo_path)
    msg = f"Sync from {info['hostname']}:{info['path']}"
    run_git(["commit", "-m", msg], cwd=repo_path)
    log_sync(repo_path, f"Created commit: {msg}", verbose)
    return True


# ---------- main ----------

def sync(repo_path: Path, remote: str = "origin", branch: str = "main",
         dry_run: bool = False, verbose: bool = False) -> bool:
    config = load_config(repo_path)

    print(f"\n{'='*60}")
    print(f"github-sync — {repo_path.name}")
    print(f"{'='*60}")
    info = get_workspace_info(repo_path)
    print(f"Repo:      {repo_path}")
    print(f"Workspace: {info['hostname']}:{info['path']}")
    print(f"Strategy:  default={config['default_strategy']}, "
          f"rules={len(config['merge_rules'])}, never_touch={len(config['never_touch'])}")
    if dry_run:
        print("Mode: DRY RUN (no changes will be made)")
    print()

    log_sync(repo_path, "=== SYNC STARTED ===", verbose)

    print("1. Checking .gitignore…")
    ensure_gitignore(repo_path, dry_run, verbose)

    print("2. Cleaning cached Python files from index…")
    clean_cached_python_files(repo_path, dry_run, verbose)

    print("3. Safety-staging all changes…")
    n = safety_stage_all(repo_path, dry_run, verbose)
    print(f"   Staged {n} files" if n else "   Nothing to stage")

    print("4. Committing staged changes…")
    print("   Created sync commit" if commit_if_needed(repo_path, dry_run, verbose) else "   No changes to commit")

    print("5. Pulling --rebase…")
    ok, msg = pull_rebase(repo_path, remote, branch, config, dry_run, verbose)
    if not ok:
        print(f"   FAILED: {msg}")
        print("\n" + "="*60)
        print("SYNC FAILED — your changes are staged and safe")
        print("Run 'git status' inside the repo to see what needs manual attention")
        print("="*60 + "\n")
        log_sync(repo_path, f"=== SYNC FAILED: {msg} ===", verbose)
        return False
    print(f"   Success: {msg}")

    print("6. Pushing to remote…")
    ok, msg = push(repo_path, remote, branch, dry_run, verbose)
    if not ok:
        print(f"   FAILED: {msg}")
        if msg == "needs_pull":
            print("   Remote has new changes. Run sync again.")
        print("\n" + "="*60)
        print("SYNC INCOMPLETE — pull succeeded but push failed")
        print("="*60 + "\n")
        log_sync(repo_path, f"=== SYNC INCOMPLETE: push failed ({msg}) ===", verbose)
        return False
    print("   Success")

    print("\n" + "="*60)
    print("SYNC COMPLETE")
    print("="*60 + "\n")
    log_sync(repo_path, "=== SYNC COMPLETE ===", verbose)
    return True


def main():
    parser = argparse.ArgumentParser(
        description="Safe Git sync for any shared repository (skills, clients, etc.)",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python sync.py                                 # Sync the repo this script lives in
  python sync.py --path active/clients           # Sync the clients submodule
  python sync.py --path active/clients --dry-run # Preview without changes
  python sync.py --verbose                       # Detailed output

Per-repo behavior is controlled by `.sync.toml` at the repo root.
With no config, the script is strict-safe: every conflict goes manual.
        """,
    )

    SCRIPT_DIR = Path(__file__).resolve().parent
    DEFAULT_PATH = SCRIPT_DIR.parent.parent  # github-sync/scripts/sync.py → repo root

    parser.add_argument(
        "--path", type=Path,
        default=Path(os.environ.get("SYNC_REPO_PATH", DEFAULT_PATH)),
        help="Path to the repo to sync (default: repo containing this script, or $SYNC_REPO_PATH)",
    )
    parser.add_argument(
        "--remote", default=os.environ.get("SYNC_REMOTE", "origin"),
        help="Git remote name (default: origin or $SYNC_REMOTE)",
    )
    parser.add_argument(
        "--branch", default=os.environ.get("SYNC_BRANCH", "main"),
        help="Branch to sync (default: main or $SYNC_BRANCH)",
    )
    parser.add_argument("--dry-run", action="store_true", help="Show what would happen without making changes")
    parser.add_argument("--verbose", "-v", action="store_true", help="Show detailed output")

    args = parser.parse_args()
    target = args.path.resolve()

    top = repo_toplevel(target)
    if top is None:
        print(f"Error: {target} is not inside a git repository.")
        sys.exit(1)

    if top != target:
        print(f"Note: resolved to repo root: {top}")
        target = top

    success = sync(
        repo_path=target,
        remote=args.remote,
        branch=args.branch,
        dry_run=args.dry_run,
        verbose=args.verbose,
    )
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
