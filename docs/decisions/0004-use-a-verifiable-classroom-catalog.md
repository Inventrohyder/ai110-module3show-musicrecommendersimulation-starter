---
status: accepted
date: 2026-07-22
decision-makers:
  - Haitham Alhad Hyder
consulted:
  - Codex desktop, GPT-5
---

# 4. Use a small, verifiable classroom catalog with disclosed annotations

## Context and problem

The starter's fictional ten-song data is useful course material but is too narrow to demonstrate broader profile behavior and a diversity adjustment on a mixed catalog. A streaming API would add unstable access, proprietary features, and licensing ambiguity to a four-hour simulation.

## Considered options

1. Keep fictional songs.
2. Import a large third-party audio-feature dataset.
3. Extend the ten starter entries with ten real recordings, verify the added recordings with MusicBrainz, and disclose student-reviewed simulation annotations.

## Decision outcome

Chosen option: **3**. The catalog preserves the ten course starter entries and adds ten MusicBrainz-verified recordings across pop, lofi, rock, electronic, ambient, jazz, and indie pop. `docs/data-provenance.md` distinguishes the starter entries from added recordings and records each added recording's source URL, verification date, and annotation policy.

## Consequences

- The catalog is usable for an authentic classroom simulation without copying protected media.
- It remains too small and manually labelled for a commercial recommendation claim.
- Repeated artists LoRoom (starter entries) and Miles Davis (added recordings) provide cases for the later diversity adjustment; the checked behavior demonstrates the LoRoom case.

## Confirmation

Haitham Alhad Hyder selected source-backed metadata in the Project 3 planning conversation on 2026-07-22 and later confirmed that the starter catalog must be extended rather than replaced. AI contribution: Codex desktop, GPT-5 assisted with source lookup and implementation. Related issue: [#5](https://github.com/Inventrohyder/ai110-module3show-musicrecommendersimulation-starter/issues/5).
