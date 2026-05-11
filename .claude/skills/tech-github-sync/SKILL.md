---
name: github-sync
description: Use when syncing any shared Git repository worked on from multiple workspaces or by multiple people — skills, clients, or any other shared submodule. Triggers include "sync skills", "sync clients", "push skills", "push clients", "pull updates", "update [the shared] repo", or any time you'd run `git pull` / `git push` in a shared submodule. Prevents data loss by staging untracked files before any destructive operation, and applies per-repo merge rules from `.sync.toml` so conflicts don't silently overwrite teammates' work.
---

# github-sync

Safe sync for any shared Git repository. Works on any repo where multiple workspaces or teammates push concurrently (skills, clients, public template repos, etc.).

## Core Safety Principle

**Stage everything before any destructive git operation.** Staged files live in git's object database and are recoverable via `git reflog`. Untracked files exist only on disk — once a `git reset --hard` or a botched rebase clobbers them, they're gone.

## Quick Reference

```bash
SYNC=".claude/skills/tech-github-sync/scripts/sync.py"

# Sync the skills repo (the script's own home)
python "$SYNC"

# Sync the clients submodule
python "$SYNC" --path active/clients

# Sync any other shared repo
python "$SYNC" --path active/{shared-repo-name}

# Preview without changes
python "$SYNC" --path active/clients --dry-run

# Detailed output
python "$SYNC" --verbose
```

## Per-repo Behavior Lives in `.sync.toml`

Drop a `.sync.toml` at the repo root to declare how conflicts should be handled. Without a config the script is **strict-safe**: every conflict falls through to manual review.

```toml
# Default applied to any file not matched by a rule.
# Use "manual" for repos with sensitive content (clients, prose).
default_strategy = "manual"

# Files that must NEVER be auto-resolved, no matter what.
never_touch = [
  "**/credentials/**",
  "**/secrets.env",
  "**/.env",
]

# Per-pattern overrides. Patterns support `**` for directory recursion.
[[merge_rules]]
match = "README.md"
strategy = "table_merge_skills_readme"   # only safe on the skills README

[[merge_rules]]
match = "**/SKILL.md"
strategy = "longer_wins"

[[merge_rules]]
match = "**/learnings.md"
strategy = "combine_unique_lines"
```

## Built-in Strategies

| Strategy | What it does | When to use |
|---|---|---|
| `manual` | Stops, archives nothing, leaves the conflict for human review | Default for any repo with prose, brand voice, or sensitive copy |
| `never_touch` | Same as `manual` but signals "this is critical" in logs | Credentials, env files |
| `combine_unique_lines` | Keeps every unique line from both sides; preserves order | Append-only logs, learnings, archives |
| `longer_wins` | Takes the longer side; archives the loser to `.conflict_archive/` | `SKILL.md` and similar where length is a reasonable proxy for completeness. Risky for prose — opt in deliberately |
| `table_merge_skills_readme` | Parses the `\| Skill \| Description \| Status \|` table, unions and sorts | Only the skills repo README |

**Nothing is ever truly lost.** When `longer_wins` discards a side, the discarded version is saved to `.conflict_archive/{timestamp}_{ours\|theirs}_{path}` at the repo root.

## What the Script Always Does

1. **Workspace audit log** — appends host + path + timestamp to `.sync_log` (gitignored).
2. **`.gitignore` hygiene** — ensures `.sync_log` is ignored; creates a baseline `.gitignore` if missing.
3. **Cache cleanup** — removes any tracked `.pyc` / `__pycache__` from the index.
4. **Safety net** — `git add .` before anything destructive.
5. **Commit** — auto-commits whatever just got staged with a workspace-tagged message.
6. **Pull --rebase** — if conflicts arise, dispatches each conflicted file to its configured strategy. If any file falls back to manual, the rebase is aborted cleanly.
7. **Push** — only after rebase succeeds. Push rejection = "run sync again to pull first," never auto-force.

## When Auto-Resolution Stops

The rebase aborts (cleanly) the moment ANY file requires manual review. Your safety-staged commit is intact; nothing has been pushed. Run `git status` inside the repo and resolve manually, then re-run sync.

## "Never Again" Rules (encoded in the script)

| Rule | Why |
|---|---|
| Never `git reset --hard` without staging first | Untracked files are gone forever |
| Never skip `git add .` before sync | Staging = backup in git's object database |
| Never force-push without explicit confirmation | Could overwrite teammates' work |
| Never auto-resolve a file matched by `never_touch` | Credentials, brand voice, etc. need eyeballs |

## Recovery

If something still goes sideways:

```bash
# Find recent states (including safety-staged snapshots)
git reflog

# Recover a file from a previous state
git checkout <sha> -- path/to/file

# If a rebase left the repo in a bad state
git rebase --abort

# Retrieve a discarded version
ls .conflict_archive/
```

## Configuration via Env Vars

| Variable | Default | Description |
|---|---|---|
| `SYNC_REPO_PATH` | parent of this script | Path to the repo to sync |
| `SYNC_REMOTE` | `origin` | Git remote name |
| `SYNC_BRANCH` | `main` | Branch to sync |

## Logging

Each sync appends to `{repo}/.sync_log` (gitignored, one log per checkout):

```
[2026-05-06T16:42:11] [walt-mbp:/path/to/repo] === SYNC STARTED ===
[2026-05-06T16:42:11] [walt-mbp:/path/to/repo] SAFETY NET: Staged 23 files
[2026-05-06T16:42:13] [walt-mbp:/path/to/repo] Pull successful
[2026-05-06T16:42:14] [walt-mbp:/path/to/repo] === SYNC COMPLETE ===
```

## Adding a New Shared Repo

1. Confirm the repo is a clean git checkout (`git status` is sane).
2. Decide your default strategy. **Start with `manual`** unless you've thought hard about edge cases.
3. Drop a `.sync.toml` at the repo root.
4. Add file globs to `never_touch` for any credentials or sensitive paths.
5. Add specific `merge_rules` only for files where auto-resolution is genuinely safe.
6. First sync: run with `--dry-run --verbose` to confirm what would happen.
