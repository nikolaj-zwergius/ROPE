# Plan: Reorder the ROPE TODO backlog

## Goal

Make the ROPE backlog a flat list ordered by priority. Keep each independently
actionable task as a separate item; represent dependent work as subtasks of a
parent task rather than grouping unrelated tasks under topic headings.

## Expected inputs

- The current tasks and priority/difficulty estimates in `TODO.md`.
- The maintainer's instruction to sort by priority, using subtasks only where
  tasks are genuinely dependent.

## Expected outputs

- Reorder `TODO.md` by priority and remove topic groupings that do not describe
  parent tasks or dependencies.
- Preserve every task's meaning and existing difficulty estimate.
- Keep genuinely dependent kissing-loop implementation steps nested under a
  clearly scoped parent task if their dependency warrants it; leave variant
  generation independent.

## Existing files and patterns to use

- `TODO.md`: current task descriptions and P1/P2 plus difficulty estimates.

## Implementation plan

1. Rewrite the backlog as a single priority-ordered list without unrelated
   topic headings.
2. Nest tasks only when one task depends on another, making that relationship
   and the shared parent outcome explicit.
3. Check that all task descriptions, priorities, and difficulty estimates are
   retained and that Markdown formatting is valid.

## Verification

- Review the resulting list for priority order, task independence, and preserved
  estimates.
- Run `git diff --check` for whitespace errors.
