# Onboarding Prompt

When a user opens this workspace for the first time and runs `/onboarding` or asks to set up their workspace, follow this script exactly.

## Instructions

1. Welcome the user: "Welcome to your Business Command Center. Let's get your workspace set up. I'll ask you a few questions one at a time."

2. Ask the following questions ONE AT A TIME. Wait for each answer before asking the next question. Do not present multiple questions at once.

   a. "What is your business name?"
   b. "What does your business do? (1-2 sentences is perfect.)"
   c. "What services or products do you offer?"
   d. "Who is your ideal customer?"
   e. "What is your website URL? (Type 'skip' if you don't have one yet.)"
   f. "Do you have any other sales pages or funnels? (Type 'skip' if not.)"
   g. "Which social media platforms are you active on? (e.g., Instagram, TikTok, YouTube, LinkedIn, Facebook)"
   h. For each platform they mention, ask: "What is your [platform] URL?"
   i. "What email platform do you use? (e.g., Mailchimp, ConvertKit, Klaviyo, ActiveCampaign — type 'skip' if none.)"

3. After all questions are answered, populate `active/BRAND.md` with their answers, replacing all placeholder text.

4. Update `CLAUDE.md` — replace "Your Business Command Center" with their business name followed by "Command Center" (e.g., "Acme Co Command Center").

5. Move this file (`ONBOARDING.md`) to `.tmp/onboarding-completed.md`.

6. Print a summary:
   - Confirm that `active/BRAND.md` has been populated
   - Confirm that `CLAUDE.md` has been updated
   - List the folder structure that is ready for use
   - Let them know they can start asking Claude to help with their business — writing emails, building landing pages, creating content, and more

## Important

- Ask questions ONE AT A TIME. Never present the full list of questions to the user.
- If the user says "skip" for any question, leave that field as "N/A" in BRAND.md.
- Keep the tone professional and helpful, not overly casual.
