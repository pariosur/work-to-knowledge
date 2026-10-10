# Output shapes

Adapt headings to the task; omit empty sections. IDs are stable machine-readable metadata, not personal information. All examples below are schematic, not completed outcomes.

## Journal

```markdown
# Task title
Task ID: stable-task-id
Status: in progress
Next: concrete next action

## Events
- event-id | ISO timestamp | decision/evidence/question/handoff: statement and evidence link
```

## Debrief

```markdown
# A specific lesson
Episode ID: stable-episode-id
Events: event-id
Journal: [Task](../journals/task.md)

## Context and observed evidence
## Decision and reasoning
## Reusable idea and limits
## Optional next step
```

## Concept

```markdown
# Concept title
Concept ID: stable-concept-id
Aliases: equivalent terms
Learning status: encountered

Plain-language definition.

## Example and limits
## Related work
## Sources
```

## Source companion (read-only original)

```markdown
# Source title
Source ID: stable-source-id
Original: [Original note](relative/path.md)
Locator: verified section/page/timestamp

## Related concepts
- [Concept](../concepts/concept.md): supported relationship and its limits
```

## Generated roadmap entry

```markdown
### Concept toward the learning objective
Status: encountered
Prerequisites: known requirements; unassessed gaps labeled unknown
Why now: connection to observed work
Next exercise: a small observable task
Evidence: none yet
Assessment: not assessed
```
