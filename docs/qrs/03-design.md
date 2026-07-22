# QRSPI — Design

Date: 2026-07-22

## Product boundary

VibeFinder is a deterministic, content-based command-line recommender for a 20-recording classroom catalog. It accepts a named profile, ranking mode, and top-k value, then prints transparent ranked results.

## Shared scoring contract

The functional API returns `(score, reasons)` for a song and ranked `(song, score, explanation)` tuples for a catalog. The `Recommender` class delegates to the same scorer so the OOP and functional paths cannot disagree.

## Planned ranking behavior

- `balanced` uses genre, mood, energy, tempo, valence, danceability, acousticness, and five advanced attributes.
- `energy-first` is a genuine alternate strategy that increases the influence of energy and tempo.
- Selection is deterministic: adjusted score descending, then title ascending.
- During top-k selection, a repeated artist receives a visible 15-point per-prior-selection adjustment. This represents catalog exposure diversity, not a general fairness claim.

## Verification boundary

Tests load the checked-in catalog and invoke the real CLI in a subprocess. A checked-in malformed CSV fixture verifies boundary errors. There are no mocked APIs or in-memory invented song catalogs.
