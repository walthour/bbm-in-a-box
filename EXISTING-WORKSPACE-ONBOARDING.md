# Adopting bbm-in-a-box in an Existing Claude Code Workspace

This doc is for someone who **already has a Claude Code workspace** and wants to adopt the bbm-in-a-box layout, skills, and conventions without losing anything they've already built.

The standard `ONBOARDING.md` assumes an empty folder. This one assumes you've already got `.claude/`, skills, clients, memory files, code, or other work in your current workspace. The goal: get you onto bbm-in-a-box's structure safely — backup first, inventory, reconcile, then rebuild in a clean sibling folder and migrate your content into it.

**Why a sibling folder instead of editing in place?** Restructuring a live workspace mid-flight is risky and hard to roll back. A sibling folder gives you a clean canvas, lets you verify everything works, and keeps the original untouched until cutover. The old folder stays as your backup.

---

## How to use this doc

1. Make sure Phase 1 of the standard `ONBOARDING.md` is done (Xcode CLT, Homebrew, Node). If you've already been using Claude Code, you almost certainly have these. Quick check:
   ```bash
   git --version && brew --version && node --version
   ```
   If any of those fail, do Phase 1 of `ONBOARDING.md` first, then come back.

2. Open a fresh Claude Code session **inside your existing workspace folder** (so Claude can see your current state).

3. Paste this entire document as the first message. Claude will follow the phases below in order.

Phases 0 (backup) and 1 (inventory) are read-only — Claude makes no destructive changes until you approve the migration plan in Phase 2.

If you want to pause at any time, just say so. Phases are sequential, not concurrent.

---

## Phase 0 — Safety backup (read + copy only)

Before any restructuring, back up the entire current workspace to a sibling folder.

```bash
# Run from the current workspace root
BACKUP_DIR="../$(basename "$(pwd)")-pre-migration-backup-$(date +%Y%m%d-%H%M%S)"
cp -R . "$BACKUP_DIR"
echo "Backup created at: $BACKUP_DIR"
```

This is a full copy including hidden files (`.git`, `.env`, `.claude/`, etc.). It lives **outside** the workspace so later cleanup can't accidentally touch it. Do not skip this step.

Claude: after creating the backup, print the backup path and confirm it's readable. Wait for the user to acknowledge before continuing.

---

## Phase 1 — Inventory (read-only)

Claude: produce a written inventory of the current workspace. **Do not modify anything yet.** The inventory is a survey to inform Phase 2 decisions.

For each item below, report what exists:

1. **Top-level files** at the workspace root — `CLAUDE.md`, `BRAND.md`, `GEMINI.md`, `README.md`, `.env`, `.gitignore`, anything else.
2. **Top-level directories** at the workspace root — list every folder name.
3. **`.claude/` contents** — `skills/`, `rules/`, `agents/`, `commands/`, `mcp-servers/`, `settings.json`, etc.
4. **Skills present** — list every folder under `.claude/skills/` with a one-line description (read each `SKILL.md`'s description field, or first heading if there's no frontmatter).
5. **Client folders** — if there's an `active/clients/` or similar, list each client folder and report its internal shape (BRAND.md? CLAUDE.md? memory/? what subdirectories?).
6. **Other `active/` content** — apps, websites, CRM/prospects, projects, anything else.
7. **Memory state** — is there a `memory/` folder? What's in it? `MAP.md`? `current/`? `decisions/`? `sessions/`?
8. **Git state** — `git remote -v`, summary of `git status` (counts only, not full file list), and `cat .gitmodules` if it exists.
9. **Existing CLAUDE.md** — read the workspace `CLAUDE.md` and summarize what conventions it enforces (in 5 bullets max).

Output as a single markdown report. Keep it under 400 lines. After printing, wait for the user to read it before moving to Phase 2.

---

## Phase 2 — Reconciliation decisions (ask, then plan)

Before restructuring, Claude must get the user's input on a few decisions. **Ask one at a time** and wait for each answer.

**Q1. Your workspace name.** What do you want the new workspace called in `CLAUDE.md` (e.g. "Sarah's Command Center")? Default: `{your first name}'s Command Center`.

**Q2. Your business name (or "personal use").** This populates `BRAND.md`. If this workspace isn't for a business, say "personal use" and we'll skip the brand questions.

**Q3. Do you do client work?** This decides whether `active/clients/` is highlighted in `CLAUDE.md` or pruned out.

**Q4. Your existing skills.** Looking at the inventory, for each skill currently under `.claude/skills/` that is NOT already in bbm-in-a-box's bundled skill list:

> "You have skill `X` that isn't part of bbm-in-a-box's bundle. Two options: (a) carry it over to the new workspace's `.claude/skills/X/` (it'll keep working), or (b) archive it under `.claude/skills/archived/X/` so it's preserved but not auto-loaded. Which do you want for `X`?"

Apply per skill. Default to (a) for skills you're actively using; (b) for stale/experimental.

For skills that already exist in bbm-in-a-box's bundle with the same name: **do not overwrite either side**. Diff the two and surface the differences to the user. They decide whether their version stays (option a, replaces the bundled one) or the bundled one wins (their version goes to `archived/`).

**Q5. Your existing clients.** For each client folder found in Phase 1:

> "Client `Y`: should this be (a) carried over to `active/clients/Y/` in the new workspace as-is, (b) carried over but restructured to match the bbm-in-a-box per-client shape (recommended for consistency), or (c) archived because the engagement ended?"

If a client folder doesn't match bbm-in-a-box's per-client shape (no `BRAND.md`, no `memory/`, etc.), default to (b) and let the user override.

**Q6. Other `active/` content.** Confirm which of `active/apps/`, `active/websites/`, `active/crm/`, etc. you want carried over. Default: all of them, as-is.

**Q7. Memory carry-over.** If the user has an existing `memory/` folder, ask:
> "Do you want to (a) carry your existing memory files over and reorganize them to match bbm-in-a-box's `memory/` shape, or (b) start fresh and archive the old memory under `memory/archived-pre-migration/`?"

After all questions are answered, Claude produces a written **migration plan**: every file/folder that will be moved, renamed, or deleted; every new structure that will be scaffolded; every skill/client decision. Print the plan and wait for explicit "yes proceed" before Phase 3.

---

## Phase 3 — Build the new workspace (sibling folder)

Rather than restructuring in place (risky), we build a **new clean workspace as a sibling folder** by cloning bbm-in-a-box into it. Once everything is migrated and verified, the user switches their Claude Code working directory to the new folder and archives the old one.

Claude: create the new workspace alongside the old one by cloning bbm-in-a-box.

```bash
# Pick the new workspace folder name (from Q1, slugified)
NEW_WORKSPACE_NAME="{slug from Q1, e.g. sarahs-command-center}"
cd ..
git clone https://github.com/walthour/bbm-in-a-box.git "$NEW_WORKSPACE_NAME"
cd "$NEW_WORKSPACE_NAME"
```

This gives the new folder a complete bbm-in-a-box scaffold: `CLAUDE.md`, `BRAND.md`, `ONBOARDING.md`, `.claude/skills/`, `memory/`, `active/`, `docs/`, etc.

Now disconnect it from the bbm-in-a-box origin so it becomes their own workspace, not a fork:

```bash
git remote remove origin
git rm -rf .git  # optional — only if they want a brand-new history
git init         # only if the rm -rf above was run
```

Most users should keep the existing git history (it's small and useful for tracking what they inherited). Only re-init if they specifically want a clean history.

---

## Phase 4 — Customize the new workspace

Claude: run the bbm-in-a-box customization flow against the new folder, using the answers already collected in Phase 2.

1. **Update `CLAUDE.md` title** — replace "Your Business Command Center" at the top with the user's workspace name from Q1.

2. **Populate `BRAND.md`** — using the business name from Q2 (or set to personal-use shape if they said "personal use"). If you don't have brand details yet, leave placeholders like `[Brand voice — to be added]` rather than inventing answers.

3. **Prune `active/clients/`** — if the user said "no client work" in Q3, archive any starter client examples in bbm-in-a-box to `.tmp/archived-starter-clients/` and update `CLAUDE.md` to remove the Clients section.

4. **Seed `memory/current/current-strategy.md`** with a one-paragraph note about what they're focused on (ask if not obvious from the inventory).

5. **Archive `ONBOARDING.md`** — since this workspace isn't going through the fresh-setup flow, move bbm-in-a-box's `ONBOARDING.md` to `.tmp/onboarding-completed.md` so it doesn't trip future sessions.

6. **Commit:**
   ```bash
   git add -A
   git commit -m "feat: customize bbm-in-a-box workspace for {workspace name}"
   ```

---

## Phase 5 — Install Superpowers (manual, Desktop-friendly)

bbm-in-a-box depends on the Superpowers skill library (brainstorming, planning, executing-plans, debugging, TDD, code review). Install it now.

**Do not run `/plugin` commands.** They're unreliable in Claude Code Desktop. Install manually as skill files instead:

```bash
# From the new workspace root
git clone https://github.com/obra/superpowers.git .tmp/superpowers-source
cp -R .tmp/superpowers-source/skills/* .claude/skills/
rm -rf .tmp/superpowers-source
git add .claude/skills/
git commit -m "feat: install Superpowers skill library"
```

After this commit, fully quit and reopen Claude Code Desktop so the new skills register. (Skip this restart if running Claude Code CLI — `claude --version` succeeds — and you prefer the marketplace install: `/plugin marketplace add obra/superpowers-marketplace` then `/plugin install superpowers@superpowers-marketplace`. The manual copy works in both surfaces though, so default to it when in doubt.)

Source: https://github.com/obra/superpowers (built by Jesse Vincent / @obra).

---

## Phase 6 — Migrate the user's existing skills

For each skill kept in Phase 2 Q4:

- **(a) Carry over** — copy the skill folder from the backup into `.claude/skills/{skill-name}/`:
  ```bash
  cp -R "$BACKUP_DIR/.claude/skills/{skill-name}" .claude/skills/
  ```

- **(b) Archive** — copy to `.claude/skills/archived/{skill-name}/`:
  ```bash
  mkdir -p .claude/skills/archived
  cp -R "$BACKUP_DIR/.claude/skills/{skill-name}" .claude/skills/archived/
  ```
  Anything under `archived/` is preserved but not auto-discovered — alert the user before invoking an archived skill in the future.

For skills the user chose to replace bundled versions with (Q4 conflict resolution): copy theirs in, archive the bundled one under `archived/`. Commit each migration so the history shows what came from where:

```bash
git add .claude/skills/
git commit -m "chore: migrate {skill-name} from previous workspace"
```

---

## Phase 7 — Migrate the user's existing clients

For each client folder kept in Phase 2 Q5:

**(a) Carry over as-is:**
```bash
cp -R "$BACKUP_DIR/active/clients/{client-name}" active/clients/
```

**(b) Carry over with restructure to per-client shape:**

1. Create the canonical structure:
   ```bash
   CLIENT="{client-name}"
   mkdir -p "active/clients/$CLIENT"/{memory/{current,decisions,sessions,meetings},active/{research,copywriting,content,projects,ads,websites},.claude/skills,assets,credentials,.tmp}
   ```
2. Walk through the old client folder and copy each file into the matching new location. When something doesn't fit a bucket, ask the user — default to `active/research/` for documents and `active/projects/{slug}/` for self-contained workstreams.
3. Create `BRAND.md` and `CLAUDE.md` at the client root if they don't exist. Pull whatever brand/integration info is recoverable from the old folder; mark unknowns with `[To be added]`.
4. Create `memory/project-brief.md` summarizing what the engagement is (one paragraph).

**(c) Archive:** move to `.tmp/archived-clients/{client-name}/` and skip.

Commit each client migration individually:

```bash
git add "active/clients/$CLIENT"
git commit -m "chore: migrate $CLIENT from previous workspace"
```

---

## Phase 8 — Migrate remaining content

What's left in the backup besides skills and clients:

- **`.env`** → copy to the new workspace root. Verify `.env` is in `.gitignore` (bbm-in-a-box ships with this, but double-check).
  ```bash
  cp "$BACKUP_DIR/.env" .env
  ```
- **`active/apps/`, `active/websites/`, `active/crm/`** → if the user has content there (from Q6), copy over as-is:
  ```bash
  cp -R "$BACKUP_DIR/active/apps/"* active/apps/ 2>/dev/null || true
  cp -R "$BACKUP_DIR/active/websites/"* active/websites/ 2>/dev/null || true
  cp -R "$BACKUP_DIR/active/crm/"* active/crm/ 2>/dev/null || true
  ```
- **Old `memory/`** — if Q7 was (a) carry-over: walk individual files into the new `memory/decisions/` or `memory/sessions/`. Don't bulk-copy the structure — the new memory shape is what matters. If Q7 was (b) start fresh: move the entire old `memory/` into `memory/archived-pre-migration/`.
- **Old `CLAUDE.md`** → archive to `memory/decisions/$(date +%Y-%m-%d)-pre-migration-claude-md.md` for reference. The new workspace `CLAUDE.md` is canonical.
- **Old `.claude/rules/`, `.claude/agents/`, `.claude/mcp-servers/`** → carry over wholesale into the matching folders in the new workspace. These rarely conflict.
- **Old `.claude/settings.json`** → diff against bbm-in-a-box's default. Port any user-specific permissions or env vars into the new file. Don't blindly overwrite — the new workspace's settings already have sensible defaults.
- **Random top-level files** → if anything was at the old workspace root that isn't `CLAUDE.md` / `BRAND.md` / `.env` / `README.md` / `.gitignore`, ask the user where it should go. Default: `.tmp/needs-sorting/`.

Commit:

```bash
git add -A
git commit -m "chore: migrate remaining workspace content"
```

---

## Phase 9 — Optional: connect MCPs

If the user is running Claude Code CLI (not Desktop), they can connect local MCPs that bbm-in-a-box skills can use. Skip this phase entirely if they're on Desktop — Desktop's cloud MCPs are configured via https://claude.ai/settings/integrations instead.

```bash
# Perplexity — web-grounded research
claude mcp add perplexity -- npx -y @perplexity-ai/mcp-server

# Firecrawl — web scraping
claude mcp add firecrawl -- npx -y firecrawl-mcp
```

After adding MCPs, restart Claude Code. Verify with `claude mcp list`.

Ask the user which API keys they have; populate the matching lines in `.env` and remind them they can add more services anytime.

---

## Phase 10 — Verify

Open a fresh Claude Code session in the new workspace and ask:

> "Read CLAUDE.md, then list the top-level folders, the skills you can see under .claude/skills/, and confirm Superpowers is installed by listing 3 skills (look for `brainstorming`, `writing-plans`, `systematic-debugging`, or similar). Then read memory/current/current-strategy.md and tell me back what's in progress. Don't do anything else."

Expected:
- Claude lists `active/`, `memory/`, `.claude/`, `docs/`
- Claude lists the bundled bbm-in-a-box skills plus any migrated ones
- Claude finds Superpowers skill folders
- Claude reads the current-strategy file

If anything's off, fix before declaring done.

Second check: pick one migrated client (if any) and ask Claude to read its `CLAUDE.md` and `BRAND.md` and report what it sees. Confirms the per-client structure works.

---

## Phase 11 — Cut over

Once verification passes:

1. Move any final straggler files from the backup into the new workspace.
2. Close the old workspace folder in Claude Code Desktop.
3. Open the new workspace folder in Claude Code Desktop. **This is now the primary workspace.**
4. Keep the backup folder for at least two weeks. After that, archive or delete:
   ```bash
   # Optional, after two weeks of confidence
   rm -rf "$BACKUP_DIR"
   ```
5. If you want a remote git host for the new workspace, set it up now:
   ```bash
   gh repo create my-workspace --private --source=. --remote=origin --push
   ```
   Or keep it local-only if you'd rather. The workspace works fine either way.

The new workspace is now structured like bbm-in-a-box, carries your old content and skills, and the old folder is preserved as a backup.

---

## Summary checklist

- [ ] Backup created in sibling folder
- [ ] Inventory of current workspace produced
- [ ] Migration plan approved by user
- [ ] New workspace cloned from bbm-in-a-box as sibling
- [ ] CLAUDE.md customized to user's workspace name
- [ ] BRAND.md populated (or set to personal-use)
- [ ] memory/current/current-strategy.md seeded
- [ ] ONBOARDING.md archived to .tmp/
- [ ] Superpowers installed manually
- [ ] User's existing skills migrated (per Q4 decisions)
- [ ] User's existing clients migrated (per Q5 decisions)
- [ ] Other active/ content (apps, websites, crm) carried over
- [ ] .env, .claude/rules/, .claude/agents/, .claude/mcp-servers/ migrated
- [ ] Old memory reconciled (per Q7 decision)
- [ ] Optional MCPs connected (CLI users only)
- [ ] Verification passes
- [ ] Cut over to new workspace, old folder preserved as backup

Welcome to bbm-in-a-box.
