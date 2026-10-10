# Validation results

Package tested locally on 2026-10-09/10 UTC. No active harness configuration, original skills, or real learning notes were changed.

## Executed checks

- Skill-creator `quick_validate.py`: passed (frontmatter, name, scaffold checks).
- Disabled example config: passed `loop_state.py validate`.
- Standard-library unit suite: **15 tests passed** after the final helper fix.
- Independent agent-interpreted forward simulation: **26 assertions passed**, **13 generated local links resolved**. It used isolated synthetic artifacts, not real journals or package example outputs as evidence.
- Package Markdown reference check: passed for real package destinations; schematic template destinations were excluded intentionally.
- Sanitization scan: no personal absolute paths, employer/client identifiers from the source setup, ticket IDs, or Obsidian wiki-links found. Manual review used generic newly written instructions and synthetic examples. This is not a legal determination of rights.

## Unit behavior covered

Selected scope and path-boundary handling; all touched roots; project configuration; global exclusions; selected topic versus excluded root; symlink exclusion; temporary no-record; ambiguous/missing context; disabled/malformed config; immediate config changes; stable event-set/task identity; prepared and committed reservations; corrupt state refusal; read-only CLI with malformed config; existing-roadmap path requirement; nonexistent work-root rejection.

Command: `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -v`

## Independent forward results

The evaluator supplied raw coding and marketing evidence and interpreted the skill to produce notes in an isolated store:

- Excluded path, symlink into exclusion, no-record, mixed, unknown, and excluded-topic contexts each passed gate/no-write assertions (12).
- Included coding and explicit marketing-topic contexts passed inclusion assertions (2).
- Incomplete coding evidence stayed pending (1).
- Prepared events stayed reserved; existing debrief identity and link marker survived a simulated crash; resume produced no duplicate debrief; committed events stayed reserved; reordered duplicate IDs remained stable (6).
- One meaningful marketing event qualified without an entry-count threshold (1).
- Existing concept and canonical source companion were reused; the read-only original's content hash remained unchanged (3).
- Roadmap `none` produced no roadmap or queue (1).

Semantic review found no fabricated deployment, launch, conversion improvement, or mastery. The coding claim stayed bounded to a controlled fixture; the marketing claim stayed bounded to a small interview sample. These are agent-interpreted simulation outcomes, not automated proof that all future model judgments will be correct.

## Finding fixed

The independent evaluator found that a nonexistent path beneath an included root could pass the helper. The helper now requires supplied work paths to exist and be readable. A new regression test passes, and the entire 15-test suite passes. The original 26-assertion simulation ran before this narrow fix; the new regression verifies the changed case. Recheck actual tool access before writes; an OS readability check cannot prove sandbox permission or eliminate filesystem races.

## Remaining limits

No live Codex, Claude Code, Pi, Gemini CLI, or Cursor installation/loading test was performed. The harness guide is supported by linked official documentation, not certification of the user's installed versions. No concurrency stress test, network filesystem transaction test, or daemon test was performed. The skill describes agent-managed locks, atomic replacements and reconciliation; the helper only evaluates scope and plans IDs/reservations. Semantic source matching, episode selection, evidence assessment and mastery assessment remain agent/user responsibilities. Future setup must verify real paths, source permissions, and instruction loading. The package is licensed under MIT and is not installed into an active harness. Publication status is separate from these local validation results.
