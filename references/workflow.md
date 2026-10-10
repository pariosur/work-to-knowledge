# Journal, episodes, and learning

## Journal and evidence

Use one stable task ID for the same work across sessions. Reuse its journal after searching the approved store's task index; do not infer identity just from a similar title. Record current purpose, observed status, next action and evidence locations. Append events with unique IDs and timestamps, each describing a decision, evidence, changed assumption, obstacle, or handoff. Correct prior mistakes with a new event referencing the old ID; preserve history. Capture rationale promptly, not just the final result. Omit secrets, personal identities, unnecessary client details and full source content. A task can stay open while several learning episodes complete.

Evidence may be an observed test result, an inspected artifact, a source passage, or a user report (label it as reported). Distinguish proposed, attempted, observed and unknown. Never turn a proposal into a completed launch, an unrun test into a passing test, or a PR opening into a merge. Log only within approved scope; minimize mixed-scope data rather than storing it and redacting later.

## Episode decision

After each meaningful journal update, read the durable checkpoint and consider pending event IDs, including deferred earlier events. Generate a debrief only when a coherent episode has:

- a consequential choice or revised understanding;
- supporting evidence with its limitations;
- a reusable conclusion or question sharpened enough to guide future work.

An inconclusive experiment can qualify if the supported conclusion is “this evidence cannot distinguish the explanations.” Routine edits, entry count, elapsed time, and task-close status alone do not qualify. One event can qualify; fifty events can remain pending. Before assigning a new episode, compare its evidence and conclusion with recent debriefs: rewording an already processed event is not new work. Reuse its event/episode identity instead of creating a second debrief. Keep related events together. Store pending IDs when recording is allowed. At a milestone, consider unresolved pending events again; do not manufacture completion. Coding adapters may notice reviewed diffs or PR milestones; marketing may use interview synthesis or experiment readouts. Neither is mandatory.

## Durable, idempotent processing

The agent owns one writer per task. Before writes, acquire an exclusive task lock using atomic directory creation under `.state/locks/TASK_ID`; if it exists, defer this loop without interrupting the main work. Do not delete an apparently stale lock without confirming the owner is inactive. Release only your own lock. This package does not implement a cross-host lock service.

Maintain `.state/TASK_ID.json` with version, task ID, pending event IDs, and an episodes map. An episode record includes its stable ID, ordered event IDs, status (`prepared` or `committed`), deterministic debrief path, concept/source links, and unfinished steps. The ID is a hash of task ID plus unique sorted event IDs; the helper provides it. Preserve this ID through recovery even if wording changes.

1. Gate and lock. Reconcile event IDs already reserved by prepared or committed episodes. Never reuse them for a new debrief. A later substantive correction is a new event and links to the earlier debrief.
2. Persist `prepared` with planned destinations and event IDs using a temporary file in the same directory and atomic replacement. Do this BEFORE writing the debrief. A prepared episode reserves its events.
3. Write `debriefs/EPISODE_ID.md` atomically with the episode ID in metadata. If it exists, verify its identity and resume missing steps; never create a second file, overwrite unrelated content, or choose a new ID to evade a conflict.
4. Add only missing concept and source links, keyed by canonical target identity, with a stable episode/link marker. Check both metadata and destination before appending. Update the prepared record after completed steps. A crash between a link write and state write is recovered by observing that link already exists.
5. Verify the debrief exists and local links resolve. Persist `committed`, retaining event IDs and destinations. Remove only those event IDs from pending. Release the lock. On resume, finish prepared episodes before evaluating new ones. If outputs disappeared, repair the original transaction or report the missing artifact; do not claim it completed again.

Do not advance a checkpoint before outputs are verified. Corrupt/missing state with existing outputs means reconcile the episode metadata first, not reset everything. Conflicting writers or identities defer processing. The helper is read-only planning logic; the agent must perform the lock and atomic file operations above. Excluded/no-record sessions never create even a lock or checkpoint. This is recoverable idempotence, not a database transaction across files.

## Debriefs and concepts

A debrief gives the context, what evidence was observed, why the choice followed, a transferable idea and its limits, and an optional next learning step. Keep it readable in a minute or two. Clearly flag synthetic examples and uncertain outcomes. Link back to the journal events.

Before creating a concept, search names, aliases and definitions in the approved concept index. Reuse semantic equivalents; different wording is not a new concept. Different ideas sharing a name need disambiguation. Use a stable concept ID, human-readable title, aliases, plain definition, grounded example, limitations, related work and sources. Ordinary Markdown links must work without Obsidian. Use URL-escaped relative destinations. Never mark mastery simply because a note or debrief exists.

## External sources and bidirectional connections

Only inspect explicitly approved source folders; search narrowly for the concept. Read the actual passage before claiming support. Store source identity (canonical path or canonical URL when provided), title, edition/date when relevant, and locator such as page/section/timestamp. Exact URL fragments can distinguish passages, but remove known tracking parameters when deduplicating a source identity. Different editions are not automatically duplicates. Do not invent a URL, quote, page number, transcript access or source conclusion. State whether a connection is direct support, analogy, contradiction, or an agent inference.

In the concept note, link the relevant source with a one-sentence supported relationship. For `read_append_links`, append only a missing concept backlink to the source's related-concepts section; preserve its text and formatting. If read-only, create/reuse a local source companion note in `sources/` that points to the original and the concept; link the concept to this companion. Thus both local notes connect in both directions without modifying the read-only original. Explain this limitation rather than claiming the original contains a backlink. Deduplicate source companions by source identity, links by canonical target, and concepts by meaning/aliases. A source revision may update the existing relationship; it is not automatically a new note.

External folders may contain copyrighted books or confidential notes: reference only necessary passages; do not duplicate whole texts. No upload or external sharing is part of the loop.

## Learning roadmap

- `none`: write no roadmap, modules, or learning queue. Concepts and debriefs can still exist.
- `existing`: read the chosen roadmap only. Link relevant entries; preserve its structure and checkboxes. Edit only if `allow_existing_updates` was approved. Record encountered concepts separately from completion/mastery.
- `generated`: grow a small roadmap only as relevant ideas recur or gaps matter to the stated objective. Connect prerequisites before recommending an advanced step. Suggest a concrete exercise or source-backed next step rather than an exhaustive curriculum.

Use distinct statuses: `encountered`, `practiced`, `demonstrated`, and `mastered`. Store dated evidence and who assessed it for promotion. Self-reported confidence is labeled self-reported, not independently demonstrated. Mastery requires the configured criterion and user review; successful task completion alone is insufficient. Keep prerequisites unknown when not assessed. Never tick someone else's existing curriculum simply because the agent wrote a note.
