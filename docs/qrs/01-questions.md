# QRSPI — Questions

Date: 2026-07-22  
Decision owner: Haitham Alhad Hyder

1. What does the course rubric require, including every stretch feature?
2. Should VibeFinder be a web app or a command-line simulation?
3. Should the catalog use fictional examples or real recordings?
4. What evidence must be captured while work happens so the final submission is reproducible?
5. Which engineering practices from the prior projects should remain, and which caused avoidable friction?

## Answers confirmed for this delivery

- The authoritative target is the supplied Project 3 rubric: 21 required points and 8 stretch points.
- This is a CLI-first classroom simulation. There is no deployment target and no Streamlit UI.
- The catalog uses real recordings with MusicBrainz identity/year verification and clearly labelled, human-reviewed simulation annotations.
- The Project board is the current task-status record. Each layer supplies its own tests, captured output, and affected documents.
- Keep Graphite, uv, Trunk, ADRs, CI, behavior-focused integration/E2E tests, and same-layer documentation. Prevent stale evidence and duplicated test setup.
