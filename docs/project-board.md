# Project-board workflow

The live board is [Music Recommender Simulation (AI110 Module 3)](https://github.com/users/Inventrohyder/projects/11). Its 13 assigned issues are the delivery source of truth.

## Fields and labels

- **Delivery status:** `Backlog`, `Ready`, `In Progress`, `In Review`, `Done`.
- **Labels:** `type:*`, `area:*`, and `priority:*` describe each issue without duplicating status.

## Required movement

1. Set an issue to `In Progress` when its Graphite branch exists.
2. Set it to `In Review` after `gt submit` creates or updates its PR.
3. Use `Closes #N` in the PR body and `Refs #N` in the commit footer.
4. After the PR closes, mark it `Done`; GitHub's closed-item automation may be enabled in the board UI when the project becomes active.

The board should use a delivery view filtered by Delivery status, a PR-review view filtered by `In Review`, and a rubric-evidence view grouped by `area:*`. These are UI views, not a second Markdown checklist.
