---
status: accepted
date: 2026-07-22
decision-makers:
  - Haitham Alhad Hyder
consulted:
  - Codex desktop, GPT-5
---

# 5. Use Strategy objects for alternative ranking modes

## Context and problem

The stretch requirement needs at least two selectable ranking approaches. Adding repeated `if mode == ...` blocks throughout the scorer would make weights, explanations, and future tests drift apart.

## Considered options

1. Add mode-specific conditionals to every score contribution.
2. Use one `RankingStrategy` value object and two concrete strategies that supply complete weight maps.

## Decision outcome

Chosen option: **2**. `BalancedStrategy` and `EnergyFirstStrategy` each own a complete normalized weight map. `get_strategy` resolves the CLI mode once; the shared scorer uses the selected strategy's weights for every contribution and explanation.

## Consequences

- New modes require one self-contained weight strategy rather than edits scattered through scoring code.
- Scores are comparable within a mode because each strategy normalizes by its own total weight.
- The two modes remain transparent heuristics, not learned machine-learning models.

## Confirmation

Haitham Alhad Hyder approved a modular Strategy implementation with balanced and energy-first modes in the Project 3 delivery plan on 2026-07-22. AI contribution: Codex desktop, GPT-5 helped identify the smallest pattern that prevents conditional drift. Related issue: [#12](https://github.com/Inventrohyder/ai110-module3show-musicrecommendersimulation-starter/issues/12).
