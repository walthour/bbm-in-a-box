# Onboarding

This walks you through getting bbm-in-a-box set up on your Mac. You'll do this once, and then you're done forever.

There are **two phases**:

- **Phase 1 — Terminal** (about 30 minutes, mostly waiting). Four commands you paste into Terminal, one at a time. This installs the macOS plumbing Claude Code needs (Git, Homebrew, Node).
- **Phase 2 — Claude Code Desktop** (about 10-15 minutes). One prompt you paste into Claude Code Desktop. It downloads this repo onto your machine, sets up everything else, and asks you a few questions about your business.

After Phase 1 finishes, **you never need to open Terminal again.** Everything from that point forward is inside Claude Code Desktop.

---

## Phase 1 — Terminal Setup

Open Terminal. (Press `Cmd+Space`, type `Terminal`, hit Enter.)

You'll paste 4 commands, one at a time. **Wait for each to fully finish before pasting the next.** Some take 10-20 minutes — that's normal.

When a command asks for your **Mac password**, type the same password you use to log into your Mac. The cursor won't move while you type — that's normal. Hit Enter when done.

---

### Step 1 of 4: Install Xcode Command Line Tools (provides Git)

This is the slowest step — expect 10-20 minutes. Paste the command, type your password when asked, then wait.

```bash
sudo softwareupdate --install "$(softwareupdate --list 2>&1 | grep -oE 'Command Line Tools for Xcode-[0-9.]+' | head -1)"
```

You'll know it's done when you see "Done." and the Terminal prompt comes back.

Verify it worked:

```bash
git --version
```

If you see something like `git version 2.39.x`, you're good. Move to Step 2.

---

### Step 2 of 4: Install Homebrew (package manager)

This will print a long block of text, then ask for your Mac password again. Type it and hit Enter. Takes 5-10 minutes.

```bash
NONINTERACTIVE=1 /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

When it finishes, it prints "Next steps" suggesting two commands. **Don't worry about those — Step 3 below handles them.**

---

### Step 3 of 4: Wire Homebrew into your shell

This makes `brew` available in every future Terminal session. No password needed.

```bash
[ -f /opt/homebrew/bin/brew ] && BREW=/opt/homebrew/bin/brew || BREW=/usr/local/bin/brew; echo "eval \"\$($BREW shellenv)\"" >> ~/.zprofile && eval "$($BREW shellenv)"
```

Verify:

```bash
brew --version
```

If you see `Homebrew 4.x.x`, you're good.

---

### Step 4 of 4: Install Node.js (runtime Claude Code uses)

Takes 2-5 minutes. No password needed.

```bash
brew install node
```

Verify:

```bash
node --version
```

If you see something like `v22.x.x`, you're done with Terminal. **You can close it now.**

---

## Phase 2 — Claude Code Desktop

1. **Create an empty folder** for your workspace. Anywhere you like — Desktop, Documents, wherever. Name it whatever you want (e.g., `bbm-in-a-box` or `My Command Center`).

2. **Open Claude Code Desktop.**

3. **Open that empty folder** in Claude Code Desktop (File → Open Folder, or the folder picker on launch).

4. **Paste this prompt** as a single message (the whole block below):

```
Bootstrap my bbm-in-a-box workspace. Do these steps in order:

1. If this folder does not already contain CLAUDE.md and ONBOARDING.md at the root, clone the bbm-in-a-box repo into the current folder using: git clone https://github.com/walthour/bbm-in-a-box.git . (note the trailing dot — it clones into the current folder, not a subfolder). If files end up in a nested subfolder, move all contents (including hidden files like .git, .claude/, .gitignore) up to the current folder root, then delete the empty subfolder.

2. Once ONBOARDING.md is at the workspace root, read it and follow the "Agent Instructions" section at the bottom exactly. Start with welcoming me, then check for Superpowers skills, then walk through the questions one at a time. Don't ask me anything else until you've read ONBOARDING.md.
```

5. Claude will start working. When it asks you questions, answer one at a time. There are about 10 questions. They take ~5 minutes.

That's it. When the questions are done, your workspace is ready.

---

---

# Agent Instructions

> The section below is for Claude (the AI), not you the user. It tells Claude what to do once you've pasted the master prompt above. You don't need to read it.

---

When invoked via the master prompt from Phase 2, the user's workspace folder already has the bbm-in-a-box repo contents at its root (CLAUDE.md, BRAND.md, ONBOARDING.md, .claude/, memory/, etc.). Phase 1 (macOS prereqs) should already be done — Git, Homebrew, and Node should be installed.

Follow these instructions exactly. Do not skip steps. Do not batch questions.

## Step 0 — Verify macOS prerequisites

Before anything else, verify the Phase 1 prerequisites are in place. Run these checks silently via Bash:

- `git --version` should succeed
- `brew --version` should succeed
- `node --version` should succeed

If any of these fail, **stop and tell the user**:

> "It looks like Phase 1 (the Terminal setup) wasn't completed. I need Git, Homebrew, and Node installed before I can finish setting up your workspace. Please open Terminal and follow the Phase 1 section at the top of ONBOARDING.md, then come back here and paste the master prompt again."

Do not attempt to install any of these from inside Claude Code Desktop — sudo password prompts don't work reliably from the Bash tool. The user must complete Phase 1 in Terminal first.

If all three checks pass, proceed to Step 1.

## Step 1 — Welcome

Say:

> "Welcome to your Business Command Center. Let's get your workspace set up. I'll ask you a few questions one at a time, then populate your brand profile and adapt the workspace to you."

## Step 2 — Check that Superpowers skills are available

Inspect `.claude/skills/` for any of these folders: `brainstorming`, `writing-plans`, `executing-plans`, `systematic-debugging`, `test-driven-development`. If at least one is present, treat Superpowers as installed and continue silently.

If NONE of those folders are present, tell the user:

> "I need to install the Superpowers skill library before we continue. I'll do this for you now — it takes about 30 seconds."

Then install it yourself by:
- Cloning `https://github.com/obra/superpowers` into `.tmp/superpowers-source/`
- Copying the contents of `.tmp/superpowers-source/skills/` into `.claude/skills/`
- Deleting `.tmp/superpowers-source/`
- Asking the user to fully quit and reopen Claude Code Desktop, then re-paste the master prompt so the new skills register.

**Do not run `/plugin` commands** — they are not reliably available in Claude Code Desktop. Always install Superpowers manually as skill files.

## Step 3 — Ask the following questions ONE AT A TIME

Wait for each answer before asking the next question. Do not present multiple questions at once.

If the user indicates this workspace is **for personal use, not a business** (says "personal", "not a business", "just for me", etc. in answer to question 3a), skip to question 3j and treat the remaining business-specific questions as N/A. Populate BRAND.md to reflect personal use rather than business voice.

a. "What is your business name? (Or, if this workspace is just for personal use, tell me 'personal use' and I'll skip the business questions.)"

b. "What does your business do? (1-2 sentences is perfect.)"

c. "What services or products do you offer?"

d. "Who is your ideal customer? (1-2 sentences describing the person, their situation, and what they want.)"

e. "What is your website URL? (Type 'skip' if you don't have one yet.)"

f. "Do you have any other sales pages or funnels? (Type 'skip' if not.)"

g. "Which social media platforms are you active on? (e.g., Instagram, TikTok, YouTube, LinkedIn, Facebook — comma separated. Type 'skip' if none.)"

h. For each platform they mention, ask: "What is your [platform] URL or handle?"

i. "What email platform do you use? (e.g., Mailchimp, ConvertKit, Klaviyo, ActiveCampaign — type 'skip' if none.)"

j. "Do you do client work? (yes/no — this affects whether the `active/clients/` folder is highlighted in your CLAUDE.md or pruned out.)"

## Step 4 — Populate `BRAND.md`

Update the file at the workspace root with their answers, replacing all placeholder text. If they said "personal use", set BRAND.md to a minimal personal-use profile (no business name, no marketing voice, just a note describing how they intend to use the workspace).

## Step 5 — Update `CLAUDE.md`

Replace the title "Your Business Command Center" at the top with their business name followed by "Command Center" (e.g., "Acme Co Command Center"). For personal-use workspaces, use the user's first name (e.g., "Wendy's Command Center").

## Step 6 — Seed `memory/current/current-strategy.md`

Write a 2-3 sentence summary of what they said they're focused on, so the file isn't empty on day one.

## Step 7 — Create a starter `.env` file

If `.env` does not already exist at the workspace root, create it with this exact content:

```
# API keys for this workspace. Fill in as you connect services.
# Lines starting with # are comments. Replace REPLACE_ME with your actual key.

# Anthropic — required if any skill calls the Claude API directly
ANTHROPIC_API_KEY=REPLACE_ME

# OpenAI — used by some skills for embeddings, transcription, or image generation
OPENAI_API_KEY=REPLACE_ME

# Perplexity — web-grounded research (used by research skills if installed)
PERPLEXITY_API_KEY=REPLACE_ME

# Firecrawl — web scraping for site research and content extraction
FIRECRAWL_API_KEY=REPLACE_ME

# Vercel — deployment of landing pages, dashboards, client deliverables
VERCEL_TOKEN=REPLACE_ME

# GitHub — needed for pushing repos that auto-deploy to Vercel
GITHUB_TOKEN=REPLACE_ME

# Add your own service-specific keys below as you connect them.
# Examples: KLAVIYO_API_KEY, GHL_API_KEY, NOTION_TOKEN, AIRTABLE_API_KEY, etc.
```

After writing the file, tell the user:

> "I created a `.env` file at the workspace root with placeholders for common API keys. Open it in any text editor and replace `REPLACE_ME` with your real keys as you connect services. You can also add more keys for any service I don't already list. Never commit this file — it's already in `.gitignore`."

## Step 8 — Archive ONBOARDING.md

Move this file (`ONBOARDING.md`) to `.tmp/onboarding-completed.md` so it doesn't re-trigger.

## Step 9 — Print a summary

Confirm:
- `BRAND.md` has been populated
- `CLAUDE.md` has been updated with the business (or personal) name
- `memory/current/current-strategy.md` has a starting note
- `.env` was created at the workspace root with placeholders (note that they need to fill it in as they connect services)
- The folder structure that's ready for use (`memory/`, `active/`, `.claude/skills/`, etc.)
- They can now ask Claude to help with their business — writing emails, building landing pages, creating content, setting up client folders, and more.

## Rules for the agent

- Ask questions ONE AT A TIME. Never present the full list of questions to the user.
- If the user says "skip" for any question, leave that field as `[Not specified]` in `BRAND.md`.
- Keep the tone professional and helpful, not overly casual.
- Do not invent details. If a field requires information the user didn't provide, leave a placeholder.
- Do not run `/plugin` slash commands at any point — they are unreliable in Claude Code Desktop.
