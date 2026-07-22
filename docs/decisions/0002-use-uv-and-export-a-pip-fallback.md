---
status: accepted
date: 2026-07-22
decision-makers:
  - Haitham Alhad Hyder
consulted:
  - Codex desktop, GPT-5
---

# 2. Use uv as the Python environment and lockfile authority

## Context and problem

The starter has an unpinned `requirements.txt` containing packages that the CLI does not need. Prior work also showed that commands accidentally run outside the intended environment can make verification non-reproducible.

## Considered options

1. Continue with an unpinned pip requirements file.
2. Use uv and a committed lockfile, while exporting pip-compatible fallback files.

## Decision outcome

Chosen option: **2**. `pyproject.toml` and `uv.lock` are authoritative. Contributors use `uv sync` and `uv run`. `requirements.txt` and `requirements-dev.txt` are generated fallback exports and are checked for parity in CI.

## Consequences

- Python is pinned to the 3.14 line for this small project.
- The development lock constrains pytest to the compatible 8.x line because pytest-bdd 8.1 emits future-removal warnings under pytest 9; the constraint keeps local and CI output clean while preserving the same BDD behavior.
- Runtime dependencies stay empty until a user-visible feature genuinely needs one.
- `pip install -r requirements*.txt` remains available for course environments that cannot install uv.

## Confirmation

Haitham Alhad Hyder approved the uv migration in the Project 3 delivery plan on 2026-07-22. AI contribution: Codex desktop, GPT-5 drafted the implementation choices. Related issue: [#2](https://github.com/Inventrohyder/ai110-module3show-musicrecommendersimulation-starter/issues/2).
