# VibeFinder contributor rules

## Delivery

- The GitHub Project is the live task-status source of truth. Markdown records decisions and evidence; it is not a second task board.
- Use Graphite for every branch, commit, restack, and pull request: `gt create`, `gt modify`, `gt restack`, and `gt submit`. Branches begin with `codex/`.
- Use `uv run` for every Python command. Do not call bare `python`, `pytest`, or `pip` in project commands.
- Keep a branch short-lived and focused on one behavior. There is no line-count target: include the tests and evidence required to make that behavior reviewable.

## Evidence and documentation

- Update the README, model card, AI-interactions log, provenance record, ADR, and changelog in the same layer whenever that layer changes their subject.
- Record only prompts actually used, commands actually run, and output actually captured. Do not invent an AI interaction or hand-write a command result.
- Treat user confirmation as the authority for accepted ADRs. Include the date, decision owner, alternatives, and consequences.
- If a review changes a lower Graphite layer, update that owning layer, restack, rerun its checks, and resubmit. Do not hide it in a later polish PR.

## Code and verification

- Prefer the standard library and the smallest shared implementation that covers the public functional and OOP APIs.
- Validate data at the CSV and CLI boundaries with useful errors.
- Exercise the checked-in catalog and real subprocess CLI. Do not use mocks, monkeypatching, synthetic in-memory song catalogs, or hand-written output fixtures.
- Before submission, run the checks named by the issue, `uv run pytest`, and `trunk check`.
