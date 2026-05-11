# Slash Commands

Custom slash commands that Claude exposes in the CLI. When you type `/{command-name}` in Claude Code, the matching file's instructions run as a workflow.

## Shape

```
.claude/commands/{command-name}.md
```

The file is a prompt that Claude executes when you invoke `/{command-name}`. It can take arguments — refer to `$ARGUMENTS` inside the file.

## Examples of useful commands

- `/save-session` — wrap up the current session and write a dated summary to `memory/sessions/`
- `/start-day` — load current strategy, next actions, and recent decisions to ground today's work
- `/promote-idea {slug}` — move `memory/ideas/{slug}.md` into a new project folder as `project-brief.md`

## Best practices

- One command per file
- Clear, imperative title at the top
- Spell out what files to read, what to write, and what to confirm with the user
- Use `$ARGUMENTS` for any user-supplied parameters
