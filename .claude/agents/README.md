# Agents

Specialized sub-agents that Claude can dispatch for focused tasks. Each agent is a self-contained capability with its own system prompt, tools, and (optionally) memory.

## Shape

```
.claude/agents/{agent-slug}/
├── AGENT.md          # System prompt + tool list + when to use
└── memory/           # Optional persistent memory for this agent
```

Or a flat single-file agent:

```
.claude/agents/{agent-slug}.md
```

## When to build an agent

- A repeating task with consistent structure (e.g. "research a new client", "audit a brand")
- A task that benefits from a focused context window separate from the main conversation
- A workflow that would otherwise need long instructions repeated in every conversation

## When NOT to build an agent

- One-off tasks → just ask Claude directly
- Anything that fits naturally in a skill → use `.claude/skills/` instead
- Plain reference material → use `memory/` or a rule under `.claude/rules/`
