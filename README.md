# Work to Knowledge

Learn from the work you do with agents, including the code they write.

An agent can finish a task while the reasoning behind it disappears into a chat. Work to Knowledge keeps the useful parts: decisions made along the way, what the evidence showed, and ideas worth understanding next. You get a record you can resume and learning notes you can return to.

![Work to Knowledge framework: agents at work feed a journal and debrief; external resources and debriefs connect to concept notes and an optional study roadmap.](assets/work-to-knowledge-overview.png)

## What you get

- **A work journal** that records decisions, surprises, obstacles, and the next step while the agent works.
- **Short debriefs** that explain what changed, why a choice made sense, and where the lesson applies.
- **Connected concept notes** that bring together your work and relevant passages from sources you approve, such as books, articles, podcasts, or research notes.
- **An optional learning roadmap** shaped around your objective and prerequisites. Encountering a concept stays separate from demonstrating mastery.

Everything is ordinary Markdown. Use your usual editor, or an Obsidian vault if you prefer. Coding, research, marketing, and operations can all use the same loop.

## A small example

Your agent fixes a retry bug. The journal records why it chose a stable request key. A local test shows that repeating the same request creates one record. The debrief explains idempotency, links an existing concept note, and suggests a small exercise to check your understanding.

That test does not establish production reliability, and reading the note does not mean you have mastered the idea. The lesson stays tied to what actually happened. See the [coding and marketing examples](references/examples.md).

## Install as a plugin

Choose the commands for your harness. These install the plugin from this repository's marketplace; they do not start recording or change your journal configuration.

### Codex

```sh
codex plugin marketplace add pariosur/work-to-knowledge
codex plugin add work-to-knowledge@work-to-knowledge
codex plugin list --json --marketplace work-to-knowledge
```

Start a new session, open `/skills` (or type `$`), and select **`work-to-knowledge:setup`**. Ask it to configure your note location, work scope, and learning preferences. The plugin also declares a Setup action for clients that support native onboarding.

The local install and skill-loading path was tested with Codex CLI **0.159.2**. If your CLI has marketplace commands but no `plugin add`, add the marketplace, restart the desktop app, and install Work to Knowledge from that source in the Plugins Directory. Check `codex plugin --help` for your version.

### Claude Code

```sh
claude plugin marketplace add pariosur/work-to-knowledge
claude plugin install work-to-knowledge@work-to-knowledge
claude plugin list
```

Start a new session and run **`/work-to-knowledge:setup`**. These commands and manifest layouts follow the official Claude Code documentation; Claude runtime loading has **not** been tested in this environment.

### One guided setup

Setup helps you choose where notes and config live, which work to include or exclude, approved source folders, and whether you want a learning roadmap. It adds one small scoped instruction to the chosen harness. Runtime notes stay outside the plugin and public repositories. Nothing is recorded until you explicitly configure it.

Already using the standalone skill? Ask setup to migrate your existing config and instruction. Use **one installation route per harness**, with one recording instruction; do not install both the native plugin and a standalone copy. Setup preserves unrelated settings and existing notes.

Scope applies before the journal is written. Say “no record this session” to pause temporarily, or “change work-to-knowledge scope” for a persistent change. Harness security prompts still apply. Installing the repository does not submit it to either vendor's official public directory.

## Portable skill and other harnesses

The original root `SKILL.md`, helper, references, templates, image, and MIT license remain available. Clone the repository:

```sh
git clone https://github.com/pariosur/work-to-knowledge.git
```

Then ask your agent, using the actual path to your clone:

> Read work-to-knowledge/SKILL.md and run its one-time setup for my harness. Help me choose scope, note location, approved sources, and optional roadmap. Preserve unrelated settings and use only one recording instruction.

### Harness setup

For a standalone install, copy only `skills/work-to-knowledge/` into the chosen skill location, or copy the root `SKILL.md`, `references/`, `assets/`, `scripts/loop_state.py`, and `LICENSE` without the repository’s native `skills/` subtree. Do not copy the whole repository beneath a skill-discovery directory: recursive discovery could load duplicate skills.

These standalone fallbacks are **documented adapters, not live-tested integrations**. The setup agent should verify loading in your installed version. The [harness guide](references/harnesses.md) includes official sources, personal/global locations, and verification steps.

| Harness | Project setup |
|---|---|
| Codex | Place the standalone skill folder in `.agents/skills/work-to-knowledge/` and add its scoped pointer to the active `AGENTS.md`. |
| Claude Code | Place it in `.claude/skills/work-to-knowledge/` and add the pointer to `CLAUDE.md`. |
| Pi | Place it in `.pi/skills/work-to-knowledge/` and add the pointer to its active `AGENTS.md`. |
| Gemini CLI | Place it in `.gemini/skills/work-to-knowledge/` and add the pointer to `GEMINI.md`. Skill activation can require Gemini's consent prompt. |
| Cursor | Keep the package in a stable local folder and point to it from a project `.cursor/rules/work-to-knowledge.mdc` rule. This is a rules-based adapter. |

You can also use Gemini CLI's documented installer, then run the one-time setup:

```sh
gemini skills install https://github.com/pariosur/work-to-knowledge.git --path skills/work-to-knowledge --scope workspace
```

This repository does not provide a generic ChatGPT local `SKILL.md` installation. Other environments need verified file access and instruction loading. Copying the package alone does not configure recording. See [setup and config changes](references/setup.md).

## How it behaves

After a meaningful journal update, the agent considers whether there is a new lesson supported by evidence. Entry counts and task closure do not force a debrief. Durable checkpoints help it resume unfinished processing and avoid repeating earlier notes.

It runs as part of an active agent workflow. It is not a daemon and cannot guarantee a callback after a session ends or crashes. External sources are limited to folders you approve. Read-only sources stay untouched; companion notes provide the return links.

## Validation and limits

The Python helper and native packaging have automated regression tests. Earlier independent synthetic scenarios passed 26 assertions. Codex native local installation and skill discovery passed in an isolated environment; Claude loading, onboarding UI, concurrent recovery, and real-world learning outcomes remain untested. Python 3 is needed for the optional helper and tests; no third-party dependencies are required.

```sh
python3 scripts/sync_plugin.py --check
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -v
```

Read the [full validation results](VALIDATION.md) and [workflow details](references/workflow.md).

## Development

Edit the portable root `SKILL.md`, `references/`, `assets/` templates, and `scripts/loop_state.py`, then run `python3 scripts/sync_plugin.py`. The committed `skills/work-to-knowledge/` bundle is generated from those files so both hosts load the same workflow and all references survive plugin caching. `skills/setup/` is the explicit setup entry point, not another recorder. Tests reject drift, missing resources, duplicate skill names, unsafe paths, and mismatched versions.

The root `plugin.json` follows the portable Agent Plugins format; `.codex-plugin/plugin.json` preserves the supported Codex compatibility format and `.claude-plugin/plugin.json` supplies Claude metadata. `.agents/plugins/marketplace.json` and `.claude-plugin/marketplace.json` both expose the same package. No active user configuration is bundled.

## Provenance and rights

The journal idea came from a colleague. The package uses newly written generic instructions and synthetic examples, with no original employer skill text, client artifacts, or private work notes bundled. Licensed under the [MIT License](LICENSE). Copyright (c) 2026 Pablo Ríos. Your notes and personal configuration belong outside this package.
