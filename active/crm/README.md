# CRM — prospects and sales pipeline

Prospects who haven't signed yet. Discovery calls, followup proposals, and research on people you're in conversation with. When a prospect converts to a client, migrate the folder from `active/crm/` to `active/clients/`.

## Folder shape

```
active/crm/{slug}/
├── README.md            # index + live proposal URL + next action
├── meeting.json         # raw call data (transcript, summary, action items)
├── analysis.md          # research + implementation plan + pricing
└── proposal/
    └── index.html       # source of truth for the proposal
```

Slug convention: `firstname-lastname` (lowercase, hyphenated), e.g. `jane-smith`.

## Rule

Never put prospect files in `.tmp/` or the workspace root. They all go under `active/crm/{slug}/`. When a prospect converts to a client, move the folder.
