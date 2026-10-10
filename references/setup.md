# One-time setup and changes

Only start setup when requested. Persist choices so the skill adds no recurring recording-permission interview. Native harness activation and security prompts, including Gemini CLI skill consent, remain in force. Existing choices in the conversation count; ask only what remains unknown, in a compact group:

1. Which scope: global, one project, or selected workspaces and/or topics? Which exclusions? Topics are stable, user-chosen labels with a short definition in the permanent instruction if needed.
2. Where should ordinary Markdown notes and config live? Keep runtime notes outside the distributable skill and outside public repositories by default. Is an Obsidian vault desired? It changes only the chosen folder.
3. Which external folders may be read (media notes, book notes, research digests)? For each, may the agent append a backlink, or only read? No folder is approved by default.
4. Learning objective, known prerequisites, and roadmap mode: existing, incrementally generated, or none? For existing, choose an exact file and whether it may be updated. Record how mastery will be evidenced.
5. Which harnesses and instruction scope should be configured? Present exact paths and small edits. A request to install/setup authorizes these chosen edits; avoid redundant approval. Draft-only requests stop at a reviewable plan.

Copy `assets/config.example.json` to the chosen config file and fill actual choices. Resolve relative paths against the config file's directory, not the working directory. Persist roots as absolute canonical paths when practical. `project` requires exactly one root and no topic selectors. `selected` means a root OR a topic may include work. `global` requires no inclusion roots/topics. Exclusions always override. For narrower intersections, select roots and use exclusions; do not silently interpret OR as AND.

`store` is the write destination. `sources` entries have `path` and `access` (`read` or `read_append_links`). Each path must be explicitly approved. Excluded paths cannot be authorized indirectly through a source. Revalidate source file canonical paths before reading/writing; a symlink must not escape an approved root. Never traverse every source just because it is allowed: search for the episode's specific concept, then inspect only candidate passages.

Create `journals/`, `debriefs/`, `concepts/`, `sources/`, and `.state/` under the store. Create `roadmap.md` only in generated mode. Use `assets/templates.md` as shape guidance, not empty boilerplate to populate everything. Persist only necessary config, no credentials. Validate with `loop_state.py validate CONFIG` before enabling. The helper validates structure, not user authorization or filesystem permissions. Do a dry-run gate for an included case, an exclusion, and an ambiguous case. Read-only “allow” does not authorize source access by itself.

Read [harnesses](harnesses.md). Inspect existing instruction files first and preserve unrelated content byte-for-byte. Add one uniquely delimited block or update only that block. Do not replace an existing file, shadow it with an override, or install the same skill twice. Existing managed policy takes precedence. Show a diff and exact config path. Verify loading with a new harmless session if authorized; otherwise report “configured, loading unverified.” Do not claim a working integration from a file write alone.

## Minimal permanent block

Fill the two path markers with actual chosen paths during setup (they are intentionally not personal paths in the package):

```markdown
<!-- work-to-knowledge:start -->
For work covered by CONFIG_PATH, follow PACKAGE_PATH/SKILL.md. Read that config before recording and before every write. Scope applies to the journal itself; exclusions, missing/ambiguous config, uncertain scope, and “no record this session” silently skip all recording. Do not ask per session. After meaningful journal updates evaluate new episodes and recover/check durable checkpoints before debriefing. Keep the user's task primary. This instruction does not authorize publication or unrelated reads/writes.
<!-- work-to-knowledge:end -->
```

For Cursor's rule file, put this body under `---\nalwaysApply: true\n---` (with real newlines). A broad loading rule still uses the config gate before recording.

## Change, pause, move, remove

On a requested change, edit only the intended config values, increment no hidden consent state, validate, and report the resulting scope. Broadening source writes requires explicit user authorization. “No record this session” stays in active conversational state; it must survive handoff/compaction in session context, not via a journal of the excluded session. A fresh unrelated session uses persisted config again. If continuity is uncertain, skip.

Disable persistently with `enabled: false`; do not delete past notes. Remove only the marked instruction block and installed skill copy when uninstall is requested. Keep notes/config unless deletion is separately requested. On moving a store, update relative links and validate them; never infer new source permission from the new location. Do not backfill skipped sessions. Catch-up reads only explicitly identified, approved journals, never private harness session archives.

## Gate context and state helper

The context JSON uses `roots` (absolute paths of every workspace/file location actually touched by this episode), `topics` (established stable labels), `scope_known` (boolean), and `no_record` (boolean). Empty roots can be used for a clearly identified topic-only task. At least a root or topic must be known, even globally. Set `scope_known: false` if the activity cannot be separated from other topics/locations; that silently skips. Do not set it true just to enable recording. The helper checks path ancestry and explicit labels; it cannot classify the conversation or verify that the supplied context is truthful or complete.

For a synthetic in-memory example, call `gate(config, {"roots": [], "topics": ["audience-research"], "scope_known": true, "no_record": false}, config_directory)` using actual Python booleans in Python code. For CLI use, pass a JSON context in approved scratch storage; delete that scratch file after use. Do not create it inside the learning store for an excluded session. CLI paths are positional arguments; quote them correctly in the shell.

The helper also exposes `episode_id(task_id, event_ids)` and `unreserved(state, event_ids)` as Python functions. Neither decides episode meaning nor writes files. `unreserved` expects a state shaped as `{"version": 1, "episodes": {"stable-id": {"status": "prepared", "events": ["event-id"]}}}`; the actual durable record also contains paths and recovery steps described in the workflow. Keep state outside the package.
