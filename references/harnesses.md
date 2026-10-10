# Harness adapters and documented limits

Official documentation checked 2026-10-09. These are documented loading mechanisms, not runtime certification of every installed version. Setup must inspect the actual harness/version and active instruction chain. Do not silently replace managed or unrelated instructions. This package does not require hooks.

| Harness | Skill location after a user chooses installation | Minimal permanent instruction target |
|---|---|---|
| Codex | Project `.agents/skills/work-learning-loop/`; user `~/.agents/skills/work-learning-loop/` | Project `AGENTS.md` or the existing active override; global `AGENTS.md` in Codex home (normally `~/.codex`). Check which file actually loads before appending. |
| Claude Code | Project `.claude/skills/work-learning-loop/`; user `~/.claude/skills/work-learning-loop/` | Existing project `CLAUDE.md` or user `~/.claude/CLAUDE.md`. Avoid relying on cross-harness AGENTS.md loading when a CLAUDE.md chain already exists. |
| Pi | Project `.pi/skills/work-learning-loop/` or `.agents/skills/work-learning-loop/`; user skill folder under the agent directory | Project `AGENTS.md` or existing active context file; global `AGENTS.md` under the agent directory (normally `~/.pi/agent`). Preserve overrides. |
| Cursor | Keep the package in a stable selected local folder; reference its SKILL.md explicitly | Project `.cursor/rules/work-learning-loop.mdc` with `alwaysApply: true`, or project `AGENTS.md`. For global loading use User Rules in Cursor settings with the same short instruction; do not invent an undocumented global rule file. |

A globally loaded instruction may point to a selected-scope config; loading is not recording permission. If a rule with the chosen name already exists, compare it and use the existing marked block or a distinct user-approved target, never overwrite it. In project mode, repeat only the tiny pointer block for selected projects, keeping one config authoritative. For Cursor global User Rules, setup can prepare the exact text; if no supported settings interface is available, the user must paste it. Report that step as pending.

Sources:

- [Codex local skills](https://developers.openai.com/codex/skills): project/user discovery paths. [Codex AGENTS.md](https://developers.openai.com/codex/guides/agents-md): global/project chain, override precedence, and instruction size limits. Restart a session to recheck changed instructions. These pages may redirect to ChatGPT Learn.
- [Claude Code skills](https://code.claude.com/docs/en/skills): personal/project skills. [Claude Code memory](https://code.claude.com/docs/en/memory): CLAUDE.md locations and conditional AGENTS.md behavior. Skills and instruction files are context, not enforced execution.
- [Pi skills](https://raw.githubusercontent.com/earendil-works/pi/main/packages/coding-agent/docs/skills.md) and [configuration](https://raw.githubusercontent.com/earendil-works/pi/main/packages/coding-agent/docs/configuration.md): skill and context loading. The former badlogic/pi-mono repository points to this upstream. Agent directory overrides can change paths. Use `/reload` after authorized changes, then verify loading.
- [Cursor rules](https://cursor.com/docs/rules.md): project `.mdc`, User Rules, and AGENTS.md. This adapter claims rule-based instruction loading only; it does not assume native skill auto-discovery or background execution.

After setup, in a fresh harmless session ask the agent to report the loaded loop instruction and evaluate a synthetic allowed/excluded context without recording. A correct file layout alone is not proof of loading. No harness was installed, configured, or live-tested while preparing this draft.
