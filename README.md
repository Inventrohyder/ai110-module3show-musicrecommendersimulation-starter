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
| **Core total**         | **72** |

### Advanced descriptors

The extended profile and catalog add release decade, mood tags, instrumentalness, liveness, and speechiness. These are student-reviewed simulation annotations, not claims about proprietary streaming analysis. The additional contributions are included in each score explanation and the combined score is normalized to 0–100.

| Additional feature           | Weight |
| ---------------------------- | -----: |
| Release-decade closeness     |      5 |
| Mood-tag overlap             |      5 |
| Instrumentalness preference  |      4 |
| Liveness closeness           |      4 |
| Speechiness closeness        |      4 |
| **Advanced-attribute total** | **22** |

### Ranking modes

`balanced` is the default. `energy-first` is a Strategy implementation that uses the same scoring engine but shifts weight from genre and mood toward energy and tempo.

| Feature              | Balanced | Energy-first |
| -------------------- | -------: | -----------: |
| Genre / mood         |  18 / 12 |       12 / 8 |
| Energy / tempo       |   12 / 8 |      25 / 15 |
| Remaining attributes |       44 |           37 |
| **Total**            |   **94** |       **97** |

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

Use `--mode balanced|energy-first` to select a ranking strategy. The CLI also accepts `--profile high-energy-pop|chill-lofi|deep-intense-rock`, `--top-k 1..20`, and `--all-profiles`.

For a pip-only course environment, install the generated fallback export with `pip install -r requirements-dev.txt`.

### Running Tests

Run the real-data and CLI tests with:

```bash
uv run pytest
```

---

## Sample Recommendation Output

`uv run python -m src.main --top-k 3` produced:

```text
VibeFinder | profile: high-energy-pop | mode: balanced

1. Sunrise City — Neon Echo | 94.76/100
   Why: genre match: +18.0/18; mood match: +12.0/12; energy similarity 0.97: +11.6/12; tempo similarity 0.85: +6.8/8; valence similarity 0.96: +7.7/8; danceability similarity 0.94: +7.5/8; acoustic preference similarity 0.82: +4.9/6; release decade similarity 0.75: +3.8/5; mood-tag overlap similarity 1.00: +5.0/5; instrumental preference similarity 1.00: +4.0/4; liveness similarity 0.97: +3.9/4; speechiness similarity 0.97: +3.9/4
2. Happy — Pharrell Williams | 93.66/100
   Why: genre match: +18.0/18; mood match: +12.0/12; energy similarity 0.97: +11.6/12; tempo similarity 0.62: +5.0/8; valence similarity 0.88: +7.0/8; danceability similarity 0.90: +7.2/8; acoustic preference similarity 0.90: +5.4/6; release decade similarity 1.00: +5.0/5; mood-tag overlap similarity 1.00: +5.0/5; instrumental preference similarity 1.00: +4.0/4; liveness similarity 0.97: +3.9/4; speechiness similarity 0.97: +3.9/4
3. Gym Hero — Max Pulse | 80.93/100
   Why: genre match: +18.0/18; mood mismatch: +0.0/12; energy similarity 0.92: +11.0/12; tempo similarity 0.97: +7.8/8; valence similarity 0.97: +7.8/8; danceability similarity 0.97: +7.8/8; acoustic preference similarity 0.95: +5.7/6; release decade similarity 0.75: +3.8/5; mood-tag overlap similarity 0.50: +2.5/5; instrumental preference similarity 1.00: +4.0/4; liveness similarity 0.94: +3.8/4; speechiness similarity 1.00: +4.0/4
```

**Screenshot or video** _(optional)_: <!-- Insert a screenshot or demo video link here -->

---

## Experiments You Tried

### Multiple-profile evaluation

```text
VibeFinder | profile: high-energy-pop | mode: balanced

1. Sunrise City — Neon Echo | 94.76/100
   Why: genre match: +18.0/18; mood match: +12.0/12; energy similarity 0.97: +11.6/12; tempo similarity 0.85: +6.8/8; valence similarity 0.96: +7.7/8; danceability similarity 0.94: +7.5/8; acoustic preference similarity 0.82: +4.9/6; release decade similarity 0.75: +3.8/5; mood-tag overlap similarity 1.00: +5.0/5; instrumental preference similarity 1.00: +4.0/4; liveness similarity 0.97: +3.9/4; speechiness similarity 0.97: +3.9/4

VibeFinder | profile: chill-lofi | mode: balanced

1. Library Rain — Paper Lanterns | 89.57/100
   Why: genre match: +18.0/18; mood match: +12.0/12; energy similarity 0.95: +11.4/12; tempo similarity 0.90: +7.2/8; valence similarity 0.95: +7.6/8; danceability similarity 0.87: +7.0/8; acoustic preference similarity 0.86: +5.2/6; release decade similarity 0.50: +2.5/5; mood-tag overlap similarity 0.50: +2.5/5; instrumental preference similarity 0.80: +3.2/4; liveness similarity 0.96: +3.8/4; speechiness similarity 0.96: +3.8/4

VibeFinder | profile: deep-intense-rock | mode: balanced

1. Everlong — Foo Fighters | 97.26/100
   Why: genre match: +18.0/18; mood match: +12.0/12; energy similarity 0.97: +11.6/12; tempo similarity 0.84: +6.7/8; valence similarity 0.98: +7.8/8; danceability similarity 0.94: +7.5/8; acoustic preference similarity 0.98: +5.9/6; release decade similarity 1.00: +5.0/5; mood-tag overlap similarity 1.00: +5.0/5; instrumental preference similarity 1.00: +4.0/4; liveness similarity 0.97: +3.9/4; speechiness similarity 0.99: +4.0/4
```

The profiles visibly move the ranking toward upbeat pop, low-energy acoustic lofi, and intense guitar rock. The lofi profile also shows a limitation: a manually assigned mood tag or genre can still outweigh a listener's nuanced personal reaction.

### Controlled energy experiment

For the verified recording **Happy** under the high-energy-pop profile, the normal score was **93.66/100**. Removing the energy contribution produced **93.17/100**. The change confirms that energy is scored, while the remaining contributions show why it is not the only factor.

### Ranking-mode experiment

For `high-energy-pop`, both modes agree on the first five rows, but a ten-result run changes the ordering: balanced ranks **Storm Runner** ahead of **Enter Sandman**, while energy-first reverses them because energy and tempo receive more weight.

The [required-rubric audit](docs/core-rubric-audit.md) maps each required point to its code, tests, and reader-facing evidence.

---

## Limitations and Risks

This is a small, manually annotated catalog. It does not understand lyrics, cultural context, production quality, accessibility needs, or changing taste. It can over-reward a profile's explicitly stated features and cannot make a collaborative-filtering claim without real interaction data. The completed [Model Card](model_card.md) expands on these limitations and planned mitigations.

---

## Reflection

The assignment's required reflection is the completed [Model Card](model_card.md). It records the intended purpose, algorithm, limitations, and improvement ideas without maintaining a second, potentially inconsistent reflection document.
