"""Behavior-focused tests over VibeFinder's checked-in catalog and APIs."""

from pathlib import Path

import pytest

from src.recommender import (
    Recommender,
    Song,
    UserProfile,
    load_songs,
    recommend_songs,
    score_song,
)

CATALOG_PATH = Path(__file__).parents[1] / "data" / "songs.csv"
MALFORMED_CATALOG_PATH = Path(__file__).parent / "fixtures" / "malformed_songs.csv"
HIGH_ENERGY_POP = {
    "genre": "pop",
    "mood": "happy",
    "energy": 0.85,
    "tempo_bpm": 130,
    "valence": 0.80,
    "danceability": 0.85,
    "likes_acoustic": False,
}


def test_checked_in_catalog_has_twenty_rows() -> None:
    assert len(load_songs(CATALOG_PATH)) == 20


def test_checked_in_catalog_preserves_the_first_starter_song() -> None:
    assert load_songs(CATALOG_PATH)[0]["title"] == "Sunrise City"


def test_checked_in_catalog_has_unique_song_ids() -> None:
    songs = load_songs(CATALOG_PATH)

    assert len({song["id"] for song in songs}) == len(songs)


def test_functional_recommendations_return_the_requested_count() -> None:
    recommendations = recommend_songs(HIGH_ENERGY_POP, load_songs(CATALOG_PATH), k=3)

    assert len(recommendations) == 3


def test_functional_recommendations_are_descending() -> None:
    recommendations = recommend_songs(HIGH_ENERGY_POP, load_songs(CATALOG_PATH), k=3)
    scores = [score for _, score, _ in recommendations]

    assert scores == sorted(scores, reverse=True)


def test_functional_recommendations_match_the_profile_genre() -> None:
    recommendations = recommend_songs(HIGH_ENERGY_POP, load_songs(CATALOG_PATH), k=3)

    assert recommendations[0][0]["genre"] == "pop"


def test_functional_recommendation_reason_includes_energy_contribution() -> None:
    recommendations = recommend_songs(HIGH_ENERGY_POP, load_songs(CATALOG_PATH), k=3)

    assert "energy similarity" in recommendations[0][2]


def test_functional_recommendation_reason_includes_acoustic_contribution() -> None:
    recommendations = recommend_songs(HIGH_ENERGY_POP, load_songs(CATALOG_PATH), k=3)

    assert "acoustic preference" in recommendations[0][2]


def _real_catalog_top_recommendations() -> tuple[UserProfile, tuple[dict, float, str], Song]:
    songs = load_songs(CATALOG_PATH)
    user = UserProfile(
        favorite_genre="pop",
        favorite_mood="happy",
        target_energy=0.85,
        likes_acoustic=False,
        target_tempo=130,
        target_valence=0.80,
        target_danceability=0.85,
    )
    functional_top = recommend_songs(user.to_preferences(), songs, k=3)[0]
    object_top = Recommender([Song.from_record(song) for song in songs]).recommend(user, k=3)[0]


    return user, functional_top, object_top


def test_oop_wrapper_matches_the_functional_top_recommendation() -> None:
    _, functional_top, object_top = _real_catalog_top_recommendations()

    assert object_top.id == functional_top[0]["id"]


def test_oop_wrapper_matches_the_functional_explanation() -> None:
    user, functional_top, object_top = _real_catalog_top_recommendations()

    assert Recommender([object_top]).explain_recommendation(user, object_top) == functional_top[2]


def test_malformed_checked_in_catalog_reports_the_boundary_problem() -> None:
    with pytest.raises(ValueError, match="energy must be between 0 and 1"):
        load_songs(MALFORMED_CATALOG_PATH)


def test_real_song_score_is_positive() -> None:
    score, _ = score_song(HIGH_ENERGY_POP, load_songs(CATALOG_PATH)[0])

    assert score > 0


def test_real_song_score_explanation_includes_energy() -> None:
    _, reasons = score_song(HIGH_ENERGY_POP, load_songs(CATALOG_PATH)[0])

    assert "energy similarity" in reasons[2]
