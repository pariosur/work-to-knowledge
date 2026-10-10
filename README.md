# Work to Knowledge Skill

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

## Get started

Clone the package into a local folder:

```sh
git clone https://github.com/pariosur/work-to-knowledge.git
```

Then ask your agent, using the actual path to your clone:

> Read work-to-knowledge/SKILL.md and run its one-time setup. Help me choose where notes live, which work to include or exclude, which source folders may be used, and whether I want a learning roadmap. Configure the appropriate skill and permanent instruction for my harness while preserving unrelated settings.

Setup saves those choices. Choose global scope, one project, or selected workspaces and topics. Scope applies before the journal is written. Say “no record this session” to pause temporarily, or “change work-to-knowledge scope” for a persistent change. The skill does not add recurring recording-permission questions; harness security prompts still apply.

### Harness setup

These are **documented adapters, not live-tested integrations**. The setup agent should verify loading in your installed version. The [harness guide](references/harnesses.md) includes official sources, personal/global locations, and verification steps.

| Harness | Project setup |
|---|---|
| Codex | Place the package in `.agents/skills/work-to-knowledge/` and add its scoped pointer to the active `AGENTS.md`. |
| Claude Code | Place it in `.claude/skills/work-to-knowledge/` and add the pointer to `CLAUDE.md`. |
| Pi | Place it in `.pi/skills/work-to-knowledge/` and add the pointer to its active `AGENTS.md`. |
| Gemini CLI | Place it in `.gemini/skills/work-to-knowledge/` and add the pointer to `GEMINI.md`. Skill activation can require Gemini's consent prompt. |
| Cursor | Keep the package in a stable local folder and point to it from a project `.cursor/rules/work-to-knowledge.mdc` rule. This is a rules-based adapter. |

You can also use Gemini CLI's documented installer, then run the one-time setup:

```sh
gemini skills install https://github.com/pariosur/work-to-knowledge.git --scope workspace
```

This repository does not provide a generic ChatGPT local `SKILL.md` installation. Other environments need verified file access and instruction loading. Copying the package alone does not configure recording. See [setup and config changes](references/setup.md).

## How it behaves

After a meaningful journal update, the agent considers whether there is a new lesson supported by evidence. Entry counts and task closure do not force a debrief. Durable checkpoints help it resume unfinished processing and avoid repeating earlier notes.

It runs as part of an active agent workflow. It is not a daemon and cannot guarantee a callback after a session ends or crashes. External sources are limited to folders you approve. Read-only sources stay untouched; companion notes provide the return links.

## Validation and limits

The Python helper passed 15 automated tests. Independent synthetic scenarios passed 26 assertions. Live harness loading, concurrent recovery, and real-world learning outcomes remain untested. Python 3 is needed for the optional helper and tests; no third-party dependencies are required.

```sh
python3 -m unittest discover -s tests -v
```

Read the [full validation results](VALIDATION.md) and [workflow details](references/workflow.md).

## Provenance and rights

The journal idea came from a colleague. The package uses newly written generic instructions and synthetic examples, with no original employer skill text, client artifacts, or private work notes bundled. Licensed under the [MIT License](LICENSE). Copyright (c) 2026 Pablo Ríos. Your notes and personal configuration belong outside this package.
