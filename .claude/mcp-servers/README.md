# Local MCP Servers

Source code for any MCP servers you build or fork locally. The Claude CLI registers MCP servers via:

```bash
claude mcp add {name} --transport stdio -- {command}
```

After adding, the server is registered in `~/.claude.json` (per-project) and surfaces its tools in your Claude Code conversations.

## When to put an MCP server here

- You forked an open-source MCP and need to maintain your local changes
- You wrote a custom MCP for a service that doesn't have one (e.g. a niche internal tool)
- You're prototyping an MCP and want it versioned with the workspace

## When NOT to put an MCP server here

- Official cloud MCPs (Notion, Slack, etc.) — those are registered via OAuth on claude.ai
- Third-party MCPs you install via package manager — those don't need to live in your repo

## Shape

```
.claude/mcp-servers/{server-name}/
├── README.md
├── pyproject.toml   # or package.json
├── src/
└── ...
```
