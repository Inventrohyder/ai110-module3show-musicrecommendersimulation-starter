# AI Interactions Log

This file records only actual AI-assisted stretch-feature work in this repository.

## Agentic Workflow (SF8)

### What task did I give the agent?

I asked Codex desktop (GPT-5) to implement the approved VibeFinder delivery plan, including the stretch requirement to add five meaningful song attributes and keep the scorer, tests, provenance, Model Card, and README consistent. The request began: **“PLEASE IMPLEMENT THIS PLAN: # VibeFinder — Project 3 Perfect-Score Delivery Plan.”**

### Prompts used

- “PLEASE IMPLEMENT THIS PLAN: # VibeFinder — Project 3 Perfect-Score Delivery Plan.”
- “You are making sure that each file that needs to be updated is updated in the very PR that it is associated with… Like the README, or the reflections, or the ai-interactions…”
- “Extend the starter catalog, not fully replacing it.”

### What did the agent generate or change?

- Preserved the ten course starter entries and extended `data/songs.csv` with ten MusicBrainz-verified recordings. The five added attributes—`release_decade`, `mood_tags`, `instrumentalness`, `liveness`, and `speechiness`—are present for all 20 catalog rows as student-reviewed simulation annotations.
- Extended the shared functional/OOP scoring path in `src/recommender.py`, including validation, normalized 0–100 scoring, and explanation text for every added contribution.
- Updated the named profiles in `src/main.py`, checked-in-catalog tests, `docs/data-provenance.md`, README weight/output evidence, and Model Card disclosure.
- Added the planned greedy artist-exposure selection rule: every previously selected song by the same artist subtracts 15 points from a remaining candidate, and the reason text shows that adjustment.
- Added the planned `tabulate` terminal table with rank, song, artist, mode, base score, final score, and wrapped score-derived reasons.

### What did I verify or fix manually?

- I reviewed the MusicBrainz identity and release-year sources for the ten added recordings in `docs/data-provenance.md` and kept all descriptor values explicitly labelled as classroom simulation annotations.
- I ran `uv run pytest`, `uv run python -m src.main --all-profiles --top-k 3`, and `trunk check` against the changed files. I also compared captured README tables with real CLI output rather than treating generated prose as evidence.
- I corrected the catalog after the user required the starter entries to be extended rather than replaced. The final catalog therefore has ten fictional course entries and ten verified additions; it does not claim that all 20 rows are real recordings.
- I checked the chill-lofi top five and confirmed that _Focus Flow_ gets the visible `-15.0` adjustment after _Midnight Coding_ by LoRoom; I updated the README and Model Card in the same diversity layer.
- I corrected stale documentation that referred to removed songs and artists, including the prior repeated-artist example.
- I ran the default, all-profiles, energy-first, and chill-lofi commands after the table change; I replaced abbreviated output evidence with exact captured tables and added CLI assertions for table headers and reasons.

## Design Pattern (SF10)

### Prompt used

- “`energy-first` is a real Strategy implementation, not a conditional scattered across the code.”

### Which design pattern did I use?

I used the **Strategy pattern**. `BalancedStrategy` and `EnergyFirstStrategy` each own one complete feature-weight map; `get_strategy` resolves the selected mode, and the shared scorer reads the strategy's weights.

### How did AI help me brainstorm or implement it?

The approved user plan required “a real Strategy implementation, not a conditional scattered across the code.” Codex desktop suggested a small shared `RankingStrategy` base with two concrete weight-owning strategies instead of factories or per-feature mode checks. The user-approved plan selected the balanced and energy-first modes; the agent implemented the focused pattern.

### How does the pattern appear in the final code?

`src/recommender.py` defines `RankingStrategy`, `BalancedStrategy`, `EnergyFirstStrategy`, and `STRATEGIES`. `recommend_songs(..., mode=...)` resolves the strategy once and passes it to `score_song`; `src/main.py` exposes `--mode balanced|energy-first`. Checked-in-catalog tests verify that energy-first changes the ordering and that the CLI accepts the mode.

### What did I verify manually?

I ran `uv run python -m src.main --profile high-energy-pop --mode energy-first --top-k 10` and compared it with the balanced result. The energy-first ranking moves _Enter Sandman_ above _Storm Runner_, so the selectable strategy has observable behavior rather than a cosmetic CLI option.
