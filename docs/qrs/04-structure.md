# QRSPI — Structure

Date: 2026-07-22

```text
src/
  recommender.py       shared domain, scoring, strategies, selection
  main.py              argparse CLI and table rendering
data/
  songs.csv            verified classroom catalog and annotations
tests/
  test_recommender.py  real-catalog integration and CLI tests
  features/            BDD scenarios over the checked-in catalog
docs/
  qrs/                 decision-stage artifacts
  decisions/           individual MADR records
  data-provenance.md   source identity and annotation policy
  rubric-audit.md      final evidence matrix
.github/workflows/     test and quality gates
```

The README is reader-facing evidence. `model_card.md` is the plain-language model disclosure. `ai_interactions.md` records only the actual stretch-feature AI workflow.
