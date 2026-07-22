# 🎵 Music Recommender Simulation

## Project Summary

VibeFinder is an explainable, content-based music recommender built for the AI110 classroom project. It ranks a deliberately small catalog against a stated taste profile; it does not learn from users or connect to a streaming service.

Your goal is to:

- Represent songs and a user "taste profile" as data
- Design a scoring rule that turns that data into recommendations
- Evaluate what your system gets right and wrong
- Reflect on how this mirrors real world AI recommenders

---

## How The System Works

Services such as Spotify and YouTube combine **input data**—song features, listening history, skips, saves, searches, and context—with **user preferences** inferred from those signals. A candidate-generation step finds plausible songs, then a ranking model estimates which candidate is most useful for the specific person and moment. The system selects the highest-ranked results while often applying diversity, safety, or business rules.

VibeFinder uses content-based filtering: it compares the attributes stored for each song with a named listener profile. Unlike collaborative filtering, it does not learn from patterns across many listeners because this classroom catalog has no interaction history. The implementation keeps the three ideas separate: song attributes are inputs, the named profile expresses preferences, and the scorer/ranker selects the top results.

### Catalog and data flow

The checked-in CSV preserves the starter's ten course-provided simulation songs and extends them with ten MusicBrainz-verified recordings. Its 20 rows span pop, lofi, rock, electronic, ambient, jazz, indie pop, and synthwave. Each row has genre, mood, energy, tempo, valence, danceability, and acousticness. Identity and release-year provenance for the added recordings, plus the annotation policy for every row, are in [data provenance](docs/data-provenance.md).

```text
CSV song attributes + named user preferences
                    │
                    ▼
            score every catalog row
                    │
                    ▼
     sort by score (then title for stable ties)
                    │
                    ▼
       top-k songs with score-derived reasons
```

### Core scoring rule

The balanced score normalizes its earned points to 0–100. Categorical features match exactly; numeric features use linear closeness. Tempo reaches zero contribution when it is 80 BPM or more away from the target. Acousticness is compared with `1.0` for an acoustic-preferring listener and `0.0` otherwise.

| Feature                | Weight |
| ---------------------- | -----: |
| Genre match            |     18 |
| Mood match             |     12 |
| Energy closeness       |     12 |
| Tempo closeness        |      8 |
| Valence closeness      |      8 |
| Danceability closeness |      8 |
| Acoustic preference    |      6 |
| **Total**              | **72** |

The scorer returns both the numeric result and each feature contribution, so a reason like `energy similarity 0.97: +11.6/12` can be checked directly against the algorithm.

---

## Getting Started

### Setup

1. Install [uv](https://docs.astral.sh/uv/) and sync the locked development environment:

   ```bash
   uv sync --locked --all-groups
   ```

2. Run the app:

   ```bash
   uv run python -m src.main
   ```

For a pip-only course environment, install the generated fallback export with `pip install -r requirements-dev.txt`.

### Running Tests

Run the real-data and CLI tests with:

```bash
uv run pytest
```

---

## Sample Recommendation Output

This is the actual output of `uv run python -m src.main --top-k 3` from the checked-in catalog.

```text
VibeFinder | profile: high-energy-pop | mode: balanced

1. Sunrise City — Neon Echo | 95.22/100
   Why: genre match: +18.0/18; mood match: +12.0/12; energy similarity 0.97: +11.6/12; tempo similarity 0.85: +6.8/8; valence similarity 0.96: +7.7/8; danceability similarity 0.94: +7.5/8; acoustic preference similarity 0.82: +4.9/6
2. Happy — Pharrell Williams | 92.06/100
   Why: genre match: +18.0/18; mood match: +12.0/12; energy similarity 0.97: +11.6/12; tempo similarity 0.62: +5.0/8; valence similarity 0.88: +7.0/8; danceability similarity 0.90: +7.2/8; acoustic preference similarity 0.90: +5.4/6
3. Gym Hero — Max Pulse | 80.64/100
   Why: genre match: +18.0/18; mood mismatch: +0.0/12; energy similarity 0.92: +11.0/12; tempo similarity 0.97: +7.8/8; valence similarity 0.97: +7.8/8; danceability similarity 0.97: +7.8/8; acoustic preference similarity 0.95: +5.7/6
```

**Screenshot or video** _(optional)_: <!-- Insert a screenshot or demo video link here -->

---

## Experiments You Tried

The profile and scoring experiments are documented with their actual output in the corresponding implementation layers.

---

## Limitations and Risks

This is a small, manually annotated catalog. It does not understand lyrics, cultural context, production quality, accessibility needs, or changing taste. It can over-reward a profile's explicitly stated features and cannot make a collaborative-filtering claim without real interaction data. The completed [Model Card](model_card.md) expands on these limitations and planned mitigations.

## Multiple-profile evaluation

This is the actual output of `uv run python -m src.main --all-profiles --top-k 3` before the later formatted-table extension.

```text
VibeFinder | profile: high-energy-pop | mode: balanced

1. Sunrise City — Neon Echo | 95.22/100
   Why: genre match: +18.0/18; mood match: +12.0/12; energy similarity 0.97: +11.6/12; tempo similarity 0.85: +6.8/8; valence similarity 0.96: +7.7/8; danceability similarity 0.94: +7.5/8; acoustic preference similarity 0.82: +4.9/6
2. Happy — Pharrell Williams | 92.06/100
   Why: genre match: +18.0/18; mood match: +12.0/12; energy similarity 0.97: +11.6/12; tempo similarity 0.62: +5.0/8; valence similarity 0.88: +7.0/8; danceability similarity 0.90: +7.2/8; acoustic preference similarity 0.90: +5.4/6
3. Gym Hero — Max Pulse | 80.64/100
   Why: genre match: +18.0/18; mood mismatch: +0.0/12; energy similarity 0.92: +11.0/12; tempo similarity 0.97: +7.8/8; valence similarity 0.97: +7.8/8; danceability similarity 0.97: +7.8/8; acoustic preference similarity 0.95: +5.7/6

VibeFinder | profile: chill-lofi | mode: balanced

1. Library Rain — Paper Lanterns | 94.89/100
   Why: genre match: +18.0/18; mood match: +12.0/12; energy similarity 0.95: +11.4/12; tempo similarity 0.90: +7.2/8; valence similarity 0.95: +7.6/8; danceability similarity 0.87: +7.0/8; acoustic preference similarity 0.86: +5.2/6
2. Midnight Coding — LoRoom | 93.31/100
   Why: genre match: +18.0/18; mood match: +12.0/12; energy similarity 0.88: +10.6/12; tempo similarity 0.97: +7.8/8; valence similarity 0.99: +7.9/8; danceability similarity 0.83: +6.6/8; acoustic preference similarity 0.71: +4.3/6
3. Focus Flow — LoRoom | 77.72/100
   Why: genre match: +18.0/18; mood mismatch: +0.0/12; energy similarity 0.90: +10.8/12; tempo similarity 1.00: +8.0/8; valence similarity 0.96: +7.7/8; danceability similarity 0.85: +6.8/8; acoustic preference similarity 0.78: +4.7/6

VibeFinder | profile: deep-intense-rock | mode: balanced

1. Everlong — Foo Fighters | 96.64/100
   Why: genre match: +18.0/18; mood match: +12.0/12; energy similarity 0.97: +11.6/12; tempo similarity 0.84: +6.7/8; valence similarity 0.98: +7.8/8; danceability similarity 0.94: +7.5/8; acoustic preference similarity 0.98: +5.9/6
2. Enter Sandman — Metallica | 95.56/100
   Why: genre match: +18.0/18; mood match: +12.0/12; energy similarity 0.99: +11.9/12; tempo similarity 0.72: +5.8/8; valence similarity 0.93: +7.4/8; danceability similarity 0.96: +7.7/8; acoustic preference similarity 1.00: +6.0/6
3. Storm Runner — Voltline | 95.08/100
   Why: genre match: +18.0/18; mood match: +12.0/12; energy similarity 0.94: +11.3/12; tempo similarity 0.91: +7.3/8; valence similarity 0.92: +7.4/8; danceability similarity 0.89: +7.1/8; acoustic preference similarity 0.90: +5.4/6
```

The profile changes visibly change the results: high-energy pop rewards upbeat, danceable pop; chill lofi shifts to low-energy, acoustic tracks; deep-intense rock shifts to high-energy rock. The lofi output also reveals a limitation: Focus Flow remains high despite its mood mismatch because the other numerical and genre terms compensate for the missing 12 mood points.

### Controlled energy experiment

For the real song **Happy** under the high-energy-pop profile, the normal score was **92.06/100**. Calling the scorer with its energy contribution removed produced **91.07/100**. That small, measurable drop makes the energy feature's effect explicit; it also shows that the result is not driven by energy alone.

---

## Reflection

The assignment's required reflection is the completed [Model Card](model_card.md). It records the intended purpose, algorithm, limitations, and improvement ideas without maintaining a second, potentially inconsistent reflection document.
