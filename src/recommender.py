"""Shared, explainable scoring for VibeFinder's classroom music catalog."""

from __future__ import annotations

import csv
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Mapping, Sequence

SongRecord = dict[str, Any]

CORE_WEIGHTS = {
    "genre": 18.0,
    "mood": 12.0,
    "energy": 12.0,
    "tempo": 8.0,
    "valence": 8.0,
    "danceability": 8.0,
    "acousticness": 6.0,
}
ADVANCED_WEIGHTS = {
    "release_decade": 5.0,
    "mood_tags": 5.0,
    "instrumentalness": 4.0,
    "liveness": 4.0,
    "speechiness": 4.0,
}
BALANCED_WEIGHTS = {**CORE_WEIGHTS, **ADVANCED_WEIGHTS}
ENERGY_FIRST_WEIGHTS = {
    "genre": 12.0,
    "mood": 8.0,
    "energy": 25.0,
    "tempo": 15.0,
    "valence": 8.0,
    "danceability": 8.0,
    "acousticness": 4.0,
    "release_decade": 4.0,
    "mood_tags": 4.0,
    "instrumentalness": 3.0,
    "liveness": 3.0,
    "speechiness": 3.0,
}
REQUIRED_COLUMNS = (
    "id",
    "title",
    "artist",
    "genre",
    "mood",
    "energy",
    "tempo_bpm",
    "valence",
    "danceability",
    "acousticness",
    "release_decade",
    "mood_tags",
    "instrumentalness",
    "liveness",
    "speechiness",
)
UNIT_INTERVAL_FIELDS = (
    "energy",
    "valence",
    "danceability",
    "acousticness",
    "instrumentalness",
    "liveness",
    "speechiness",
)


class RankingStrategy:
    """A named, self-contained set of feature weights for one ranking mode."""

    def __init__(self, name: str, weights: Mapping[str, float]):
        self.name = name
        self.weights = dict(weights)

    @property
    def total_weight(self) -> float:
        """Return the normalization denominator for this strategy."""
        return sum(self.weights.values())


class BalancedStrategy(RankingStrategy):
    """The general-purpose mode that gives every supported feature its documented weight."""

    def __init__(self) -> None:
        super().__init__("balanced", BALANCED_WEIGHTS)


class EnergyFirstStrategy(RankingStrategy):
    """A mode that makes energy and tempo the strongest ranking signals."""

    def __init__(self) -> None:
        super().__init__("energy-first", ENERGY_FIRST_WEIGHTS)


STRATEGIES = {
    "balanced": BalancedStrategy(),
    "energy-first": EnergyFirstStrategy(),
}


def get_strategy(strategy: str | RankingStrategy) -> RankingStrategy:
    """Resolve a public mode name or accept a strategy object for direct use."""
    if isinstance(strategy, RankingStrategy):
        return strategy
    try:
        return STRATEGIES[strategy]
    except KeyError as error:
        choices = ", ".join(STRATEGIES)
        raise ValueError(f"unknown ranking mode {strategy!r}; choose one of: {choices}") from error


@dataclass(frozen=True)
class Song:
    """A song and the attributes used by the initial content-based score."""

    id: int
    title: str
    artist: str
    genre: str
    mood: str
    energy: float
    tempo_bpm: float
    valence: float
    danceability: float
    acousticness: float
    release_decade: int = 2010
    mood_tags: tuple[str, ...] = ()
    instrumentalness: float = 0.0
    liveness: float = 0.0
    speechiness: float = 0.0

    @classmethod
    def from_record(cls, record: Mapping[str, Any]) -> "Song":
        """Create a typed song from a validated catalog record."""
        return cls(**validate_song_record(record))

    def to_record(self) -> SongRecord:
        """Return the functional API representation of this song."""
        return {
            "id": self.id,
            "title": self.title,
            "artist": self.artist,
            "genre": self.genre,
            "mood": self.mood,
            "energy": self.energy,
            "tempo_bpm": self.tempo_bpm,
            "valence": self.valence,
            "danceability": self.danceability,
            "acousticness": self.acousticness,
            "release_decade": self.release_decade,
            "mood_tags": self.mood_tags,
            "instrumentalness": self.instrumentalness,
            "liveness": self.liveness,
            "speechiness": self.speechiness,
        }


@dataclass(frozen=True)
class UserProfile:
    """A user's content preferences, with sensible defaults for numeric targets."""

    favorite_genre: str
    favorite_mood: str
    target_energy: float
    likes_acoustic: bool
    target_tempo: float = 120.0
    target_valence: float = 0.5
    target_danceability: float = 0.5
    target_release_decade: int = 2010
    desired_mood_tags: tuple[str, ...] = ("neutral",)
    likes_instrumental: bool = False
    target_liveness: float = 0.5
    target_speechiness: float = 0.2

    def to_preferences(self) -> SongRecord:
        """Return the dictionary accepted by the functional scoring API."""
        return {
            "genre": self.favorite_genre,
            "mood": self.favorite_mood,
            "energy": self.target_energy,
            "likes_acoustic": self.likes_acoustic,
            "tempo_bpm": self.target_tempo,
            "valence": self.target_valence,
            "danceability": self.target_danceability,
            "release_decade": self.target_release_decade,
            "mood_tags": self.desired_mood_tags,
            "likes_instrumental": self.likes_instrumental,
            "liveness": self.target_liveness,
            "speechiness": self.target_speechiness,
        }


class Recommender:
    """An OOP façade that delegates ranking to the functional scoring engine."""

    def __init__(self, songs: Sequence[Song]):
        self.songs = list(songs)

    def recommend(self, user: UserProfile, k: int = 5, mode: str = "balanced") -> list[Song]:
        """Return the same ranked songs as :func:`recommend_songs`."""
        ranked = recommend_songs(user.to_preferences(), [song.to_record() for song in self.songs], k, mode)
        by_id = {song.id: song for song in self.songs}
        return [by_id[record["id"]] for record, _, _ in ranked]

    def explain_recommendation(self, user: UserProfile, song: Song, mode: str = "balanced") -> str:
        """Explain this song using the same score contributions used for ranking."""
        _, reasons = score_song(user.to_preferences(), song.to_record(), strategy=mode)
        return "; ".join(reasons)


def _as_float(value: Any, field: str) -> float:
    """Convert a numeric CSV value or raise a boundary-focused error."""
    try:
        return float(value)
    except (TypeError, ValueError) as error:
        raise ValueError(f"{field} must be numeric, got {value!r}") from error


def _unit_interval(value: Any, field: str) -> float:
    """Validate a normalized catalog or preference value."""
    number = _as_float(value, field)
    if not 0.0 <= number <= 1.0:
        raise ValueError(f"{field} must be between 0 and 1, got {number}")
    return number


def _release_decade(value: Any, field: str) -> int:
    """Validate an integer decade used as a transparent era preference."""
    try:
        decade = int(value)
    except (TypeError, ValueError) as error:
        raise ValueError(f"{field} must be a decade such as 2010, got {value!r}") from error
    if not 1900 <= decade <= 2020 or decade % 10:
        raise ValueError(f"{field} must be a decade from 1900 through 2020, got {decade}")
    return decade


def _mood_tags(value: Any, field: str) -> tuple[str, ...]:
    """Normalize a pipe-delimited CSV field or a profile tag collection."""
    raw_tags = value.split("|") if isinstance(value, str) else value
    try:
        tags = tuple(tag.strip().casefold() for tag in raw_tags if tag.strip())
    except TypeError as error:
        raise ValueError(f"{field} must be pipe-delimited text or a tag collection") from error
    if not tags:
        raise ValueError(f"{field} must include at least one tag")
    return tags


def validate_song_record(record: Mapping[str, Any]) -> SongRecord:
    """Validate and normalize one CSV record before it reaches scoring logic."""
    missing = [column for column in REQUIRED_COLUMNS if column not in record]
    if missing:
        raise ValueError(f"song record is missing required columns: {', '.join(missing)}")
    try:
        song_id = int(record["id"])
    except (TypeError, ValueError) as error:
        raise ValueError(f"id must be an integer, got {record['id']!r}") from error
    if song_id < 1:
        raise ValueError(f"id must be positive, got {song_id}")

    normalized = {"id": song_id}
    for field in ("title", "artist", "genre", "mood"):
        value = str(record[field]).strip()
        if not value:
            raise ValueError(f"{field} must not be blank")
        normalized[field] = value
    for field in UNIT_INTERVAL_FIELDS:
        normalized[field] = _unit_interval(record[field], field)
    tempo = _as_float(record["tempo_bpm"], "tempo_bpm")
    if tempo <= 0:
        raise ValueError(f"tempo_bpm must be positive, got {tempo}")
    normalized["tempo_bpm"] = tempo
    normalized["release_decade"] = _release_decade(record["release_decade"], "release_decade")
    normalized["mood_tags"] = _mood_tags(record["mood_tags"], "mood_tags")
    return normalized


def load_songs(csv_path: str | Path) -> list[SongRecord]:
    """Load a valid catalog from CSV, rejecting malformed rows with useful errors."""
    path = Path(csv_path)
    if not path.is_file():
        raise FileNotFoundError(f"song catalog not found: {path}")
    with path.open(newline="", encoding="utf-8") as catalog_file:
        reader = csv.DictReader(catalog_file)
        if reader.fieldnames is None:
            raise ValueError("song catalog needs a header row")
        missing = [column for column in REQUIRED_COLUMNS if column not in reader.fieldnames]
        if missing:
            raise ValueError(f"song catalog is missing required columns: {', '.join(missing)}")
        songs = []
        for row_number, row in enumerate(reader, start=2):
            try:
                songs.append(validate_song_record(row))
            except ValueError as error:
                raise ValueError(f"invalid song catalog row {row_number}: {error}") from error
    if not songs:
        raise ValueError("song catalog must include at least one song")
    ids = [song["id"] for song in songs]
    if len(ids) != len(set(ids)):
        raise ValueError("song catalog ids must be unique")
    return songs


def _preference_value(preferences: Mapping[str, Any], *keys: str, default: Any) -> Any:
    """Return the first supplied preference key, preserving starter key names."""
    for key in keys:
        if key in preferences:
            return preferences[key]
    return default


def _normalize_preferences(user_prefs: Mapping[str, Any]) -> SongRecord:
    """Validate functional or OOP-style user preferences at the scoring boundary."""
    genre = str(_preference_value(user_prefs, "genre", "favorite_genre", default="")).strip()
    mood = str(_preference_value(user_prefs, "mood", "favorite_mood", default="")).strip()
    if not genre or not mood:
        raise ValueError("user preferences need non-empty genre and mood values")
    likes_acoustic = _preference_value(user_prefs, "likes_acoustic", default=False)
    if not isinstance(likes_acoustic, bool):
        raise ValueError("likes_acoustic must be true or false")
    likes_instrumental = _preference_value(user_prefs, "likes_instrumental", default=False)
    if not isinstance(likes_instrumental, bool):
        raise ValueError("likes_instrumental must be true or false")
    return {
        "genre": genre,
        "mood": mood,
        "energy": _unit_interval(
            _preference_value(user_prefs, "energy", "target_energy", default=0.5),
            "target energy",
        ),
        "tempo_bpm": _as_float(
            _preference_value(user_prefs, "tempo_bpm", "target_tempo", default=120.0),
            "target tempo_bpm",
        ),
        "valence": _unit_interval(
            _preference_value(user_prefs, "valence", "target_valence", default=0.5),
            "target valence",
        ),
        "danceability": _unit_interval(
            _preference_value(user_prefs, "danceability", "target_danceability", default=0.5),
            "target danceability",
        ),
        "likes_acoustic": likes_acoustic,
        "release_decade": _release_decade(
            _preference_value(user_prefs, "release_decade", "target_release_decade", default=2010),
            "target release_decade",
        ),
        "mood_tags": _mood_tags(
            _preference_value(user_prefs, "mood_tags", "desired_mood_tags", default=("neutral",)),
            "target mood_tags",
        ),
        "likes_instrumental": likes_instrumental,
        "liveness": _unit_interval(
            _preference_value(user_prefs, "liveness", "target_liveness", default=0.5),
            "target liveness",
        ),
        "speechiness": _unit_interval(
            _preference_value(user_prefs, "speechiness", "target_speechiness", default=0.2),
            "target speechiness",
        ),
    }


def _similarity(actual: float, target: float, span: float) -> float:
    """Return a clipped, linear similarity score between zero and one."""
    return max(0.0, 1.0 - abs(actual - target) / span)


def _feature_reason(name: str, earned: float, weight: float, detail: str) -> str:
    """Format one score contribution for human-readable ranking explanations."""
    return f"{name} {detail}: +{earned:.1f}/{weight:.0f}"


def score_song(
    user_prefs: Mapping[str, Any],
    song: Mapping[str, Any] | Song,
    *,
    strategy: str | RankingStrategy = "balanced",
    include_energy: bool = True,
) -> tuple[float, list[str]]:
    """Return a 0–100 content score and the exact contributions that produced it."""
    record = song.to_record() if isinstance(song, Song) else validate_song_record(song)
    preferences = _normalize_preferences(user_prefs)
    ranking_strategy = get_strategy(strategy)
    weights = ranking_strategy.weights
    reasons = []

    genre_match = record["genre"].casefold() == preferences["genre"].casefold()
    genre_score = weights["genre"] if genre_match else 0.0
    reasons.append(_feature_reason("genre", genre_score, weights["genre"], "match" if genre_match else "mismatch"))

    mood_match = record["mood"].casefold() == preferences["mood"].casefold()
    mood_score = weights["mood"] if mood_match else 0.0
    reasons.append(_feature_reason("mood", mood_score, weights["mood"], "match" if mood_match else "mismatch"))

    energy_weight = weights["energy"] if include_energy else 0.0
    energy_similarity = _similarity(record["energy"], preferences["energy"], 1.0)
    energy_score = energy_weight * energy_similarity
    energy_detail = f"similarity {energy_similarity:.2f}" if include_energy else "excluded for experiment"
    reasons.append(_feature_reason("energy", energy_score, energy_weight, energy_detail))

    tempo_similarity = _similarity(record["tempo_bpm"], preferences["tempo_bpm"], 80.0)
    tempo_score = weights["tempo"] * tempo_similarity
    reasons.append(_feature_reason("tempo", tempo_score, weights["tempo"], f"similarity {tempo_similarity:.2f}"))

    valence_similarity = _similarity(record["valence"], preferences["valence"], 1.0)
    valence_score = weights["valence"] * valence_similarity
    reasons.append(_feature_reason("valence", valence_score, weights["valence"], f"similarity {valence_similarity:.2f}"))

    dance_similarity = _similarity(record["danceability"], preferences["danceability"], 1.0)
    dance_score = weights["danceability"] * dance_similarity
    reasons.append(
        _feature_reason("danceability", dance_score, weights["danceability"], f"similarity {dance_similarity:.2f}")
    )

    acoustic_target = 1.0 if preferences["likes_acoustic"] else 0.0
    acoustic_similarity = _similarity(record["acousticness"], acoustic_target, 1.0)
    acoustic_score = weights["acousticness"] * acoustic_similarity
    reasons.append(
        _feature_reason("acoustic preference", acoustic_score, weights["acousticness"], f"similarity {acoustic_similarity:.2f}")
    )

    decade_similarity = _similarity(record["release_decade"], preferences["release_decade"], 40.0)
    decade_score = weights["release_decade"] * decade_similarity
    reasons.append(
        _feature_reason("release decade", decade_score, weights["release_decade"], f"similarity {decade_similarity:.2f}")
    )

    shared_tags = set(record["mood_tags"]) & set(preferences["mood_tags"])
    tag_similarity = len(shared_tags) / len(preferences["mood_tags"])
    tag_score = weights["mood_tags"] * tag_similarity
    reasons.append(
        _feature_reason("mood-tag overlap", tag_score, weights["mood_tags"], f"similarity {tag_similarity:.2f}")
    )

    instrumental_target = 1.0 if preferences["likes_instrumental"] else 0.0
    instrumental_similarity = _similarity(record["instrumentalness"], instrumental_target, 1.0)
    instrumental_score = weights["instrumentalness"] * instrumental_similarity
    reasons.append(
        _feature_reason(
            "instrumental preference",
            instrumental_score,
            weights["instrumentalness"],
            f"similarity {instrumental_similarity:.2f}",
        )
    )

    liveness_similarity = _similarity(record["liveness"], preferences["liveness"], 1.0)
    liveness_score = weights["liveness"] * liveness_similarity
    reasons.append(
        _feature_reason("liveness", liveness_score, weights["liveness"], f"similarity {liveness_similarity:.2f}")
    )

    speechiness_similarity = _similarity(record["speechiness"], preferences["speechiness"], 1.0)
    speechiness_score = weights["speechiness"] * speechiness_similarity
    reasons.append(
        _feature_reason(
            "speechiness", speechiness_score, weights["speechiness"], f"similarity {speechiness_similarity:.2f}"
        )
    )

    earned = (
        genre_score
        + mood_score
        + energy_score
        + tempo_score
        + valence_score
        + dance_score
        + acoustic_score
        + decade_score
        + tag_score
        + instrumental_score
        + liveness_score
        + speechiness_score
    )
    available_weight = ranking_strategy.total_weight if include_energy else ranking_strategy.total_weight - weights["energy"]
    return round(100.0 * earned / available_weight, 2), reasons


def recommend_songs(
    user_prefs: Mapping[str, Any],
    songs: Sequence[Mapping[str, Any] | Song],
    k: int = 5,
    mode: str = "balanced",
) -> list[tuple[SongRecord, float, str]]:
    """Score every song and return a deterministic, descending top-k list."""
    strategy = get_strategy(mode)
    if not 1 <= k <= len(songs):
        raise ValueError(f"k must be between 1 and {len(songs)}")
    scored = []
    for song in songs:
        record = song.to_record() if isinstance(song, Song) else validate_song_record(song)
        score, reasons = score_song(user_prefs, record, strategy=strategy)
        scored.append((record, score, "; ".join(reasons)))
    return sorted(scored, key=lambda item: (-item[1], item[0]["title"].casefold()))[:k]
