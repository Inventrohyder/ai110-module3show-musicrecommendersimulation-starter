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
CORE_WEIGHT_TOTAL = sum(CORE_WEIGHTS.values())
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
)
UNIT_INTERVAL_FIELDS = ("energy", "valence", "danceability", "acousticness")


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
        }


class Recommender:
    """An OOP façade that delegates ranking to the functional scoring engine."""

    def __init__(self, songs: Sequence[Song]):
        self.songs = list(songs)

    def recommend(self, user: UserProfile, k: int = 5) -> list[Song]:
        """Return the same ranked songs as :func:`recommend_songs`."""
        ranked = recommend_songs(user.to_preferences(), [song.to_record() for song in self.songs], k)
        by_id = {song.id: song for song in self.songs}
        return [by_id[record["id"]] for record, _, _ in ranked]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        """Explain this song using the same score contributions used for ranking."""
        _, reasons = score_song(user.to_preferences(), song.to_record())
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
    }


def _similarity(actual: float, target: float, span: float) -> float:
    """Return a clipped, linear similarity score between zero and one."""
    return max(0.0, 1.0 - abs(actual - target) / span)


def _feature_reason(name: str, earned: float, weight: float, detail: str) -> str:
    """Format one score contribution for human-readable ranking explanations."""
    return f"{name} {detail}: +{earned:.1f}/{weight:.0f}"


def score_song(user_prefs: Mapping[str, Any], song: Mapping[str, Any] | Song) -> tuple[float, list[str]]:
    """Return a 0–100 content score and the exact contributions that produced it."""
    record = song.to_record() if isinstance(song, Song) else validate_song_record(song)
    preferences = _normalize_preferences(user_prefs)
    reasons = []

    genre_match = record["genre"].casefold() == preferences["genre"].casefold()
    genre_score = CORE_WEIGHTS["genre"] if genre_match else 0.0
    reasons.append(
        _feature_reason("genre", genre_score, CORE_WEIGHTS["genre"], "match" if genre_match else "mismatch")
    )

    mood_match = record["mood"].casefold() == preferences["mood"].casefold()
    mood_score = CORE_WEIGHTS["mood"] if mood_match else 0.0
    reasons.append(
        _feature_reason("mood", mood_score, CORE_WEIGHTS["mood"], "match" if mood_match else "mismatch")
    )

    energy_similarity = _similarity(record["energy"], preferences["energy"], 1.0)
    energy_score = CORE_WEIGHTS["energy"] * energy_similarity
    reasons.append(_feature_reason("energy", energy_score, CORE_WEIGHTS["energy"], f"similarity {energy_similarity:.2f}"))

    tempo_similarity = _similarity(record["tempo_bpm"], preferences["tempo_bpm"], 80.0)
    tempo_score = CORE_WEIGHTS["tempo"] * tempo_similarity
    reasons.append(_feature_reason("tempo", tempo_score, CORE_WEIGHTS["tempo"], f"similarity {tempo_similarity:.2f}"))

    valence_similarity = _similarity(record["valence"], preferences["valence"], 1.0)
    valence_score = CORE_WEIGHTS["valence"] * valence_similarity
    reasons.append(_feature_reason("valence", valence_score, CORE_WEIGHTS["valence"], f"similarity {valence_similarity:.2f}"))

    dance_similarity = _similarity(record["danceability"], preferences["danceability"], 1.0)
    dance_score = CORE_WEIGHTS["danceability"] * dance_similarity
    reasons.append(
        _feature_reason("danceability", dance_score, CORE_WEIGHTS["danceability"], f"similarity {dance_similarity:.2f}")
    )

    acoustic_target = 1.0 if preferences["likes_acoustic"] else 0.0
    acoustic_similarity = _similarity(record["acousticness"], acoustic_target, 1.0)
    acoustic_score = CORE_WEIGHTS["acousticness"] * acoustic_similarity
    reasons.append(
        _feature_reason("acoustic preference", acoustic_score, CORE_WEIGHTS["acousticness"], f"similarity {acoustic_similarity:.2f}")
    )

    earned = genre_score + mood_score + energy_score + tempo_score + valence_score + dance_score + acoustic_score
    return round(100.0 * earned / CORE_WEIGHT_TOTAL, 2), reasons


def recommend_songs(
    user_prefs: Mapping[str, Any],
    songs: Sequence[Mapping[str, Any] | Song],
    k: int = 5,
    mode: str = "balanced",
) -> list[tuple[SongRecord, float, str]]:
    """Score every song and return a deterministic, descending top-k list."""
    if mode != "balanced":
        raise ValueError("only the balanced ranking mode is available until the strategy extension")
    if not 1 <= k <= len(songs):
        raise ValueError(f"k must be between 1 and {len(songs)}")
    scored = []
    for song in songs:
        record = song.to_record() if isinstance(song, Song) else validate_song_record(song)
        score, reasons = score_song(user_prefs, record)
        scored.append((record, score, "; ".join(reasons)))
    return sorted(scored, key=lambda item: (-item[1], item[0]["title"].casefold()))[:k]
