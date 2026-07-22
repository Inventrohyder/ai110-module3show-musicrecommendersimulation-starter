# Model Card: VibeFinder

## 1. Model Name

**VibeFinder 1.0** is an explainable, content-based music recommender simulation.

---

## 2. Intended Use

VibeFinder is for classroom exploration of how a recommender turns attributes and stated preferences into a ranked list. It recommends songs from a fixed 20-recording catalog for a user who supplies a genre, mood, and numeric taste targets. It is not a streaming product or a prediction about real listeners.

---

## 3. How the Model Works

Each song has genre, mood, energy, tempo, valence, danceability, acousticness, release decade, mood tags, instrumentalness, liveness, and speechiness. A profile provides a preferred genre and mood plus target values and tags. VibeFinder gives points for genre/mood matches, tag overlap, and numerical closeness, then divides by the available points to make a 0–100 score. A Strategy object selects either the balanced weights or an energy-first emphasis; the final list is sorted from high to low and each row states the same contributions used by the score.

---

## 4. Data

The catalog has 20 songs across eight broad genres: the ten course-provided starter simulation entries plus ten MusicBrainz-verified recordings. Five added attributes—release decade, mood tags, instrumentalness, liveness, and speechiness—extend the original feature set. All feature values are student-reviewed simulation annotations rather than provider audio analysis. The catalog is intentionally small, so many artists, languages, communities, and musical traditions are absent.

---

## 5. Strengths

The three real CLI profiles show the intended broad behavior: the high-energy-pop profile ranks Sunrise City first, chill-lofi ranks Library Rain first, and deep-intense-rock ranks Everlong first. Reasons expose every contribution, so a reader can see both strong matches and trade-offs instead of treating the score as a black box.

---

## 6. Limitations and Bias

Manual annotations and an uneven tiny catalog can encode the curator's judgement. Exact genre/mood matching can overfit one label and hide songs that a person might enjoy for other reasons. For example, chill-lofi can still rank Focus Flow despite its mood mismatch because genre and numerical similarity compensate. The catalog is also heavily English-language and has no real listener interaction data. A later artist-diversity adjustment reduces repetition but does not make a broad fairness guarantee.

---

## 7. Evaluation

Automated tests load the checked-in CSV, reject a checked-in malformed CSV, compare the functional and OOP APIs, verify that a verified song's release-decade preference affects a score, and run the real command in a subprocess. BDD scenarios exercise high-energy-pop, chill-lofi, and deep-intense-rock against the same catalog. The actual CLI runs selected Sunrise City, Library Rain, and Everlong respectively. A controlled experiment removed Happy's energy contribution: its score changed from 93.66 to 93.17. A second experiment confirms that energy-first moves Enter Sandman above Storm Runner in a ten-result high-energy-pop ranking.

---

## 8. Future Work

The completed five transparent attributes and two ranking modes improve profile expressiveness, but they do not remove manual-annotation bias. Diversity-aware selection and a formatted explanation table should be checked with the same real catalog. A production system would need consented interaction data, a larger balanced catalog, user studies, accessibility and language coverage, and monitoring for disparate outcomes.

---

## 9. Optional Personal Reflection

I learned that a recommendation score can look precise while still depending on subjective feature definitions and hand-chosen weights. Comparing the three profiles made the ranking behavior easy to predict, but LoRoom's visible repeat-artist adjustment showed why explanation is not the same as correctness: the system can clearly explain why Focus Flow loses 15 points while a listener might still prefer it. This simulation made me more aware that real recommenders need richer data, user control, and careful bias evaluation rather than only a larger scoring formula.
