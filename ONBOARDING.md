# Onboarding Prompt

When a user opens this workspace for the first time and runs `/onboarding` or asks to set up their workspace, follow this script exactly.

## Instructions

1. **Welcome the user.** Say:
   > "Welcome to your Business Command Center. Let's get your workspace set up. I'll ask you a few questions one at a time, then populate your brand profile and adapt the workspace to you."

2. **Ask the following questions ONE AT A TIME.** Wait for each answer before asking the next question. Do not present multiple questions at once.

   a. "What is your business name?"
   b. "What does your business do? (1-2 sentences is perfect.)"
   c. "What services or products do you offer?"
   d. "Who is your ideal customer? (1-2 sentences describing the person, their situation, and what they want.)"
   e. "What is your website URL? (Type 'skip' if you don't have one yet.)"
   f. "Do you have any other sales pages or funnels? (Type 'skip' if not.)"
   g. "Which social media platforms are you active on? (e.g., Instagram, TikTok, YouTube, LinkedIn, Facebook — comma separated)"
   h. For each platform they mention, ask: "What is your [platform] URL or handle?"
   i. "What email platform do you use? (e.g., Mailchimp, ConvertKit, Klaviyo, ActiveCampaign — type 'skip' if none.)"
   j. "Do you do client work? (yes/no — this just affects whether the `active/clients/` folder is highlighted in your CLAUDE.md or pruned out.)"

3. **Populate `BRAND.md`** at the workspace root with their answers, replacing all placeholder text.

4. **Update `CLAUDE.md`** — replace the title "Your Business Command Center" at the top with their business name followed by "Command Center" (e.g., "Acme Co Command Center").

5. **Update `memory/current/current-strategy.md`** with a 2-3 sentence summary of what they said they're focused on, so the file isn't empty on day one.

6. **Move this file** (`ONBOARDING.md`) to `.tmp/onboarding-completed.md` so it doesn't re-trigger.

7. **Print a summary** that confirms:
   - `BRAND.md` has been populated
   - `CLAUDE.md` has been updated with the business name
   - `memory/current/current-strategy.md` has a starting note
   - The folder structure that's ready for use (`memory/`, `active/`, `.claude/skills/`, etc.)
   - They can now ask Claude to help with their business — writing emails, building landing pages, creating content, setting up client folders, and more.

## Important

- Ask questions ONE AT A TIME. Never present the full list of questions to the user.
- If the user says "skip" for any question, leave that field as `[Not specified]` in `BRAND.md`.
- Keep the tone professional and helpful, not overly casual.
- Do not invent details. If a field requires information the user didn't provide, leave a placeholder.
