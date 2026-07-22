# Model Card: VibeFinder

## 1. Model Name

**VibeFinder 1.0** is an explainable, content-based music recommender simulation.

---

## 2. Intended Use

VibeFinder is for classroom exploration of how a recommender turns attributes and stated preferences into a ranked list. It recommends songs from a fixed 20-recording catalog for a user who supplies a genre, mood, and numeric taste targets. It is not a streaming product or a prediction about real listeners.

---

## 3. How the Model Works

Each song has genre, mood, energy, tempo, valence, danceability, and acousticness. A profile provides a preferred genre and mood plus target values. VibeFinder gives points for genre/mood matches and partial points when numerical values are close to the target, then divides by the available points to make a 0–100 score. The final list is sorted from high to low and each row states the same contributions used by the score.

---

## 4. Data

The catalog has 20 songs across eight broad genres: the ten course-provided starter simulation entries plus ten MusicBrainz-verified recordings. Feature values are student-reviewed simulation annotations rather than provider audio analysis. The catalog is intentionally small, so many artists, languages, communities, and musical traditions are absent.

---

## 5. Strengths

The completed profile evaluation will record observed strengths from real CLI runs.

---

## 6. Limitations and Bias

Manual annotations and an uneven tiny catalog can encode the curator's judgement. Exact genre/mood matching can overfit one label and hide songs that a person might enjoy for other reasons. The later evaluation adds a controlled experiment and a documented diversity adjustment.

---

## 7. Evaluation

The checked-in catalog is loaded and ranked in automated integration tests; the completed evaluation will add three distinct CLI profile runs.

---

## 8. Future Work

The planned extensions add five transparent attributes, a second strategy, diversity-aware selection, and a formatted explanation table. A production system would need consented interaction data, a larger balanced catalog, user studies, and monitoring for disparate outcomes.

---

## 9. Personal Reflection

The completed profile evaluation will add the student's reflection after examining actual outputs.
