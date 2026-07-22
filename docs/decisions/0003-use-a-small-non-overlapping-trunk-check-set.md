---
status: accepted
date: 2026-07-22
decision-makers:
  - Haitham Alhad Hyder
consulted:
  - Codex desktop, GPT-5
---

# 3. Use a small, non-overlapping Trunk quality check set

## Context and problem

The starter enables both Ruff and separate Black/isort tooling, plus checks that do not directly support this small CLI. Overlapping formatters create avoidable review churn and slow feedback.

## Considered options

1. Keep every inherited check.
2. Use Ruff for Python lint and import ordering, plus focused Markdown/YAML, workflow, security, secret, and diff checks.

## Decision outcome

Chosen option: **2**. Trunk runs Ruff, markdownlint, Prettier, actionlint, Bandit, TruffleHog, and git-diff-check. Black, isort, Grype, and OSV scanner are removed from this course repository's local check set.

## Consequences

- There is one Python lint/import-order authority instead of competing tools.
- Security vulnerability scanning is handled by locked dependency review in CI rather than duplicating unrelated scanners locally.
- Pre-commit formatting and pre-push checking stay enabled through Trunk hooks.
- Markdownlint keeps its structural rules, while MD013 is disabled so captured fixed-width
  CLI output and source URLs can remain verbatim evidence.
- Trunk's shared configuration and linter configs are versioned; generated runtime files
  remain ignored through `.trunk/.gitignore`.

## Confirmation

Haitham Alhad Hyder approved the non-overlapping Trunk setup in the Project 3 delivery plan on 2026-07-22. AI contribution: Codex desktop, GPT-5 drafted the trade-off summary. Related issue: [#3](https://github.com/Inventrohyder/ai110-module3show-musicrecommendersimulation-starter/issues/3).
