---
name: setup
description: Set up Work to Knowledge or change its note location, scope, sources, and learning preferences when the user explicitly asks. Never use merely because the plugin was installed or configuration is missing.
disable-model-invocation: true
---

# Set up Work to Knowledge

Run only for an explicit setup or configuration-change request. This is the setup entry point, not a second recording workflow.

Read [the canonical bundled setup procedure](../work-to-knowledge/references/setup.md) and [the main skill](../work-to-knowledge/SKILL.md). Paths are relative to this skill file, not the current working directory. Follow their scope, privacy, and permission rules.

1. Inspect the active harness and instruction chain. Detect an existing standalone or plugin installation and its marked instruction block before changing anything. Reuse an existing config only when its exact path is established by the user or current instruction. Never search personal folders for it.
2. Ask only unanswered choices, in one compact group: note/config location, work scope and exclusions, approved source folders and their read/backlink permissions, optional learning roadmap, and which harness/instruction scope to configure. With no approved external sources, keep `sources: []`. Keep runtime data outside the plugin cache and public repositories.
3. Start from the bundled disabled config example. Complete and validate the user's choices before enabling. Do not overwrite their existing config with the example or broaden permissions on an upgrade. Test synthetic included, excluded, and ambiguous contexts without writing notes.
4. Add or update exactly one marked permanent instruction for this harness, using the plugin-aware block in the setup reference. Refer to the installed skill by its verified identity, not a versioned plugin-cache path. Preserve unrelated instructions. Do not install a standalone skill on top of the plugin or add lifecycle hooks. If migrating, explain and remove only the superseded instruction/copy within the user's authorization; if removal is not authorized, pause before enabling the duplicate.
5. Show the precise config path, resulting scope, small instruction diff, and actual test results. Verify the installed main skill is discoverable in a fresh harmless session if possible. Otherwise label loading unverified. Installing a plugin alone never enables recording.

Do not fabricate choices, write a journal as a setup test, publish notes, or configure another harness unless requested.
