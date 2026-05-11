# Apps

Standalone applications you build — internal tools, customer-facing apps, dashboards, deliverables hubs, anything that has its own dependencies and deploys somewhere.

Each app folder is self-contained: own `package.json` / `pyproject.toml` / etc., own `.env` if needed, own README.

## Suggested shape

```
active/apps/{app-slug}/
├── README.md         # what this app does, how to run it
├── package.json      # (or pyproject.toml, etc.)
├── .env.example      # template for required env vars
├── src/
└── ...
```

Run apps from within their own folder:

```bash
cd active/apps/{app-slug}
npm install && npm run dev
```
