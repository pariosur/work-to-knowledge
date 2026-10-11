# Harness adapters and documented limits

Official documentation checked 2026-10-10. These are documented loading mechanisms, not runtime certification of every installed version. Setup must inspect the actual harness/version and active instruction chain. Do not silently replace managed or unrelated instructions. This package does not require hooks.

| Harness | Skill location after a user chooses installation | Minimal permanent instruction target |
|---|---|---|
| Codex | Project `.agents/skills/work-to-knowledge/`; user `~/.agents/skills/work-to-knowledge/` | Project `AGENTS.md` or the existing active override; global `AGENTS.md` in Codex home (normally `~/.codex`). Check which file actually loads before appending. |
| Claude Code | Project `.claude/skills/work-to-knowledge/`; user `~/.claude/skills/work-to-knowledge/` | Existing project `CLAUDE.md` or user `~/.claude/CLAUDE.md`. Avoid relying on cross-harness AGENTS.md loading when a CLAUDE.md chain already exists. |
| Pi | Project `.pi/skills/work-to-knowledge/` or `.agents/skills/work-to-knowledge/`; user skill folder under the agent directory | Project `AGENTS.md` or existing active context file; global `AGENTS.md` under the agent directory (normally `~/.pi/agent`). Preserve overrides. |
| Gemini CLI | Project `.gemini/skills/work-to-knowledge/`; user `~/.gemini/skills/work-to-knowledge/` (also supports `.agents/skills` aliases) | Project `GEMINI.md`; global `~/.gemini/GEMINI.md`. Preserve existing context and configured filename overrides. |
| Cursor | Keep the package in a stable selected local folder; reference its SKILL.md explicitly | Project `.cursor/rules/work-to-knowledge.mdc` with `alwaysApply: true`, or project `AGENTS.md`. For global loading use User Rules in Cursor settings with the same short instruction; do not invent an undocumented global rule file. |

For a standalone adapter, install only the self-contained `skills/work-to-knowledge/` folder from the repository, or assemble the original root skill and its resources without the native `skills/` subtree. Do not copy the whole repository inside a recursive skill-discovery directory. A globally loaded instruction may point to a selected-scope config; loading is not recording permission. If a rule with the chosen name already exists, compare it and use the existing marked block or a distinct user-approved target, never overwrite it. In project mode, repeat only the tiny pointer block for selected projects, keeping one config authoritative. For Cursor global User Rules, setup can prepare the exact text; if no supported settings interface is available, the user must paste it. Report that step as pending.

Sources:

- [Codex local skills](https://developers.openai.com/codex/skills): project/user discovery paths. [Codex AGENTS.md](https://developers.openai.com/codex/guides/agents-md): global/project chain, override precedence, and instruction size limits. Restart a session to recheck changed instructions. These pages may redirect to ChatGPT Learn.
- [Claude Code skills](https://code.claude.com/docs/en/skills): personal/project skills. [Claude Code memory](https://code.claude.com/docs/en/memory): CLAUDE.md locations and conditional AGENTS.md behavior. Skills and instruction files are context, not enforced execution.
- [Pi skills](https://raw.githubusercontent.com/earendil-works/pi/main/packages/coding-agent/docs/skills.md) and [configuration](https://raw.githubusercontent.com/earendil-works/pi/main/packages/coding-agent/docs/configuration.md): skill and context loading. The former badlogic/pi-mono repository points to this upstream. Agent directory overrides can change paths. Use `/reload` after authorized changes, then verify loading.
- [Cursor rules](https://cursor.com/docs/rules.md): project `.mdc`, User Rules, and AGENTS.md. This adapter claims rule-based instruction loading only; it does not assume native skill auto-discovery or background execution.

After setup, in a fresh harmless session ask the agent to report the loaded loop instruction and evaluate a synthetic allowed/excluded context without recording. A correct file layout alone is not proof of loading. Standalone adapters were not live-tested. Native plugin test results are described below and in the repository validation report.

## Native Codex and Claude Code plugins

The repository also provides native manifests, a shared `skills/` bundle, and repository marketplaces. Prefer this route for Codex and Claude Code; the table above remains the portable fallback. Choose one route per harness. Native installation does not install the permanent scope pointer or grant access to a note store; invoke the setup skill afterward.

- Codex: add the repository with `codex plugin marketplace add pariosur/work-to-knowledge`, then `codex plugin add work-to-knowledge@work-to-knowledge`. CLI 0.159.2 was tested for local marketplace installation and namespaced skill loading. Older clients may offer marketplace management but require installing through the desktop Plugins Directory. Check `codex plugin --help` instead of assuming a command exists.
- Claude Code: `claude plugin marketplace add pariosur/work-to-knowledge`, then `claude plugin install work-to-knowledge@work-to-knowledge`. Start a new session and run `/work-to-knowledge:setup`. This route is documented and structurally checked, but no Claude runtime test was performed here.
- Codex setup: select the installed plugin's Setup action when supported, or ask it to run the installed `work-to-knowledge:setup` skill. The manifest declares onboarding; the UI action itself is not runtime-tested.

[OpenAI packaging and marketplace documentation](https://developers.openai.com/plugins/build/plugins), [Claude Code plugin reference](https://code.claude.com/docs/en/plugins-reference), and [Claude marketplace guide](https://code.claude.com/docs/en/plugin-marketplaces) describe the formats and installation routes. The native package contains no hooks, MCP servers, remote services, credentials, or scheduled background recorder. Publishing this Git repository is not approval/listing in either vendor's public plugin directory.

## Gemini CLI

[Agent Skills](https://geminicli.com/docs/cli/skills/) documents local skill discovery, `gemini skills install URL --path skills/work-to-knowledge --scope workspace`, `/skills list`, and `/skills reload`. Workspace scope avoids the installer's user-scope default. Native activation presents a consent prompt; this package cannot suppress or promise to eliminate it. Do not bypass harness safeguards. Skill-directory access does not by itself authorize access to the separate note store.

[GEMINI.md context](https://geminicli.com/docs/cli/gemini-md/) documents project and global context files. Add the small scoped pointer block from setup to the existing active context file, reload with `/memory reload`, and inspect `/memory show`. Verify the skill appears in `/skills list` and dry-run the gate without recording. This is documented Gemini CLI support, not a claim about the Gemini web app, live integration testing, or background execution.
