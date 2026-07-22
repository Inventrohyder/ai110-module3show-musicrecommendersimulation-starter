# Required-rubric audit

Audit date: 2026-07-22  
Scope: the 21 required points only; stretch evidence is audited separately after each extension.

| Required feature                  | Evidence                                                                                                                                                                                            | Automated check                                                                      | Manual check                                                  |
| --------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------ | ------------------------------------------------------------- |
| Clear recommender explanation (3) | [README: Catalog and algorithm](../README.md#catalog-and-algorithm) distinguishes inputs, user preferences, ranking, content-based, and collaborative filtering.                                    | Markdown/Trunk checks.                                                               | Read for coherent plain-language explanation.                 |
| Structured song dataset (3)       | [`data/songs.csv`](../data/songs.csv) contains ten starter entries and ten verified additions with seven core attributes; [provenance](data-provenance.md) discloses sources and annotation policy. | `test_checked_in_catalog_loads_twenty_valid_songs`.                                  | Open the CSV and confirm the breadth of genres.               |
| Preference scoring (3)            | [`score_song`](../src/recommender.py) applies documented weights and returns a numeric 0–100 score plus individual reasons.                                                                         | `test_real_song_score_includes_the_designed_energy_feature`.                         | Compare one reason with the README weight table.              |
| Sorted recommendations (3)        | [`recommend_songs`](../src/recommender.py) scores all rows and sorts by score then title; CLI exposes top-k.                                                                                        | `test_functional_recommendations_are_descending_and_explained`; CLI subprocess test. | Run `uv run python -m src.main --top-k 3`.                    |
| Explanations (3)                  | Every CLI row prints the same contributions used by the score; [captured result](../README.md#transparent-table-output) includes three readable examples.                                           | `test_functional_recommendations_are_descending_and_explained`.                      | Check that each listed reason matches its score contribution. |
| Multiple profiles (3)             | High-energy-pop, chill-lofi, and deep-intense-rock output and comparison are in [README](../README.md#multiple-profile-evaluation).                                                                 | Three BDD scenarios and `test_real_cli_runs_all_three_named_profiles`.               | Run `uv run python -m src.main --all-profiles --top-k 3`.     |
| Completed Model Card (3)          | [`model_card.md`](../model_card.md) covers purpose, data, method, observed behavior, limitations/bias, evaluation, and future work.                                                                 | Markdown/Trunk checks.                                                               | Read against the rubric's three Model Card criteria.          |

## Gate result

All seven required features have code, test, and reader-facing evidence. `uv run pytest` reports 13 passing tests at this gate. No new product changes belong in this audit layer: any discovery must be absorbed into the owning layer and restacked before review.

## Reproducible gate commands

```bash
uv run pytest
trunk check --all --no-progress
uv run python -m src.main --all-profiles --top-k 3
```
