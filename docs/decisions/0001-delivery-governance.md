---
status: accepted
date: 2026-07-22
decision-makers:
  - Haitham Alhad Hyder
consulted:
  - Codex desktop, GPT-5
---

# 1. Use QRSPI records, a GitHub Project, and Graphite layers

## Context and problem

Prior projects showed that strong code can still lose credit or create rework when documentation, AI evidence, and board status lag the implementation. This project needs a small workflow that makes review evidence visible without creating a second task tracker.

## Decision drivers

- Keep the current task status accurate.
- Make each change easy to review and trace to rubric evidence.
- Preserve explicit human decisions while acknowledging actual AI assistance.

## Considered options

1. Keep a long Markdown checklist as the live plan.
2. Use a GitHub Project as the live board and use static QRSPI/ADR records for decisions and evidence.
3. Use no formal tracking beyond commits.

## Decision outcome

Chosen option: **2**. GitHub Project 11 is the live board. QRSPI records capture questions, research, design, and structure; each zero-padded ADR captures one durable decision. Graphite creates short-lived, dependent review layers.

## Consequences

- Every issue and PR must carry its evidence and update affected reader-facing documents in the same layer.
- Markdown does not duplicate changing board status.
- A lower-layer correction is absorbed into that layer and restacked, increasing a little command discipline in exchange for an honest history.

## Confirmation

Haitham Alhad Hyder approved this workflow in the Project 3 planning conversation on 2026-07-22. AI contribution: Codex desktop, GPT-5 assisted with research synthesis and drafting; the human owner selected the process and scope. Related issue: [#1](https://github.com/Inventrohyder/ai110-module3show-musicrecommendersimulation-starter/issues/1).
