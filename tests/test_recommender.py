"""Behavior-focused tests over VibeFinder's checked-in catalog and real CLI."""

import subprocess
import sys
from pathlib import Path

import pytest

from src.main import USER_PROFILES
from src.recommender import (
    Recommender,
    Song,
    SongRecord,
    UserProfile,
    load_songs,
    recommend_songs,
    score_song,
)

CATALOG_PATH = Path(__file__).parents[1] / "data" / "songs.csv"
MALFORMED_CATALOG_PATH = Path(__file__).parent / "fixtures" / "malformed_songs.csv"
PROJECT_ROOT = Path(__file__).parents[1]
HIGH_ENERGY_POP = {
    "genre": "pop",
    "mood": "happy",
    "energy": 0.85,
    "tempo_bpm": 130,
    "valence": 0.80,
    "danceability": 0.85,
    "likes_acoustic": False,
    "release_decade": 2010,
    "mood_tags": ("dance", "uplifting"),
    "likes_instrumental": False,
    "liveness": 0.12,
    "speechiness": 0.05,
}


@pytest.fixture
def happy_song() -> dict[str, object]:
    """Provide the checked-in MusicBrainz-verified Happy row for score experiments."""
    return load_songs(CATALOG_PATH)[10]


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


def _run_cli(*arguments: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, "-m", "src.main", *arguments],
        cwd=PROJECT_ROOT,
        capture_output=True,
        check=False,
        text=True,
    )

def test_real_cli_default_profile_exits_successfully() -> None:
    assert _run_cli("--top-k", "3").returncode == 0


def test_real_cli_default_profile_includes_the_transparent_table_columns() -> None:
    assert "Base score" in _run_cli("--top-k", "3").stdout


def test_real_cli_default_profile_identifies_its_profile_and_mode() -> None:
    assert "VibeFinder | profile: high-energy-pop | mode: balanced" in _run_cli("--top-k", "3").stdout

def test_real_cli_default_profile_has_the_expected_first_recommendation() -> None:
    assert "Sunrise City" in _run_cli("--top-k", "3").stdout


def test_real_cli_default_profile_explains_the_first_recommendation() -> None:
    assert "genre match: +18.0/18" in _run_cli("--top-k", "3").stdout


def test_real_cli_rejects_an_out_of_range_top_k_with_a_nonzero_status() -> None:
    assert _run_cli("--top-k", "21").returncode != 0


def test_real_cli_rejects_an_out_of_range_top_k_with_a_clear_error() -> None:
    assert "top-k must be between 1 and 20" in _run_cli("--top-k", "21").stderr


def test_named_profiles_change_the_real_catalog_recommendation() -> None:
    songs = load_songs(CATALOG_PATH)
    pop_top = recommend_songs(HIGH_ENERGY_POP, songs, k=1)[0][0]["title"]
    lofi_top = recommend_songs(
        {
            "genre": "lofi",
            "mood": "chill",
            "energy": 0.30,
            "tempo_bpm": 80,
            "valence": 0.55,
            "danceability": 0.45,
            "likes_acoustic": True,
        },
        songs,
        k=1,
    )[0][0]["title"]
    rock_top = recommend_songs(
        {
            "genre": "rock",
            "mood": "intense",
            "energy": 0.85,
            "tempo_bpm": 145,
            "valence": 0.40,
            "danceability": 0.55,
            "likes_acoustic": False,
        },
        songs,
        k=1,
    )[0][0]["title"]

    assert {pop_top, lofi_top, rock_top} == {"Sunrise City", "Library Rain", "Storm Runner"}


def test_energy_removal_experiment_changes_a_verified_song_score(happy_song: dict[str, object]) -> None:
    with_energy, _ = score_song(HIGH_ENERGY_POP, happy_song)
    without_energy, _ = score_song(HIGH_ENERGY_POP, happy_song, include_energy=False)

    assert with_energy != without_energy


def test_energy_removal_experiment_explains_the_excluded_feature(happy_song: dict[str, object]) -> None:
    _, reasons = score_song(HIGH_ENERGY_POP, happy_song, include_energy=False)

    assert "energy excluded for experiment" in reasons[2]


def test_advanced_release_decade_preference_changes_a_verified_song_score(
    happy_song: dict[str, object],
) -> None:
    matching_score, _ = score_song(HIGH_ENERGY_POP, happy_song)
    earlier_era = {**HIGH_ENERGY_POP, "release_decade": 1950}
    earlier_score, _ = score_song(earlier_era, happy_song)

    assert matching_score > earlier_score


def test_advanced_release_decade_preference_appears_in_its_reason(
    happy_song: dict[str, object],
) -> None:
    _, reasons = score_song(HIGH_ENERGY_POP, happy_song)

    assert "release decade similarity 1.00" in reasons[7]


def test_advanced_mood_tags_appear_in_their_reason(happy_song: dict[str, object]) -> None:
    _, reasons = score_song(HIGH_ENERGY_POP, happy_song)

    assert "mood-tag overlap" in reasons[8]


def test_real_cli_runs_all_named_profiles_successfully() -> None:
    assert _run_cli("--all-profiles", "--top-k", "3").returncode == 0


@pytest.mark.parametrize(
    "profile_name",
    ("high-energy-pop", "chill-lofi", "deep-intense-rock"),
)
def test_real_cli_includes_each_named_profile(profile_name: str) -> None:
    assert f"profile: {profile_name}" in _run_cli("--all-profiles", "--top-k", "3").stdout


@pytest.mark.parametrize(
    ("mode", "expected_rank_seven_title"),
    (
        pytest.param(
            "balanced",
            "Storm Runner",
            id="balanced-rank-seven-is-storm-runner",
        ),
        pytest.param(
            "energy-first",
            "Enter Sandman",
            id="energy-first-rank-seven-is-enter-sandman",
        ),
    ),
)
def test_ranking_strategy_places_expected_song_at_rank_seven(
    real_catalog: list[SongRecord],
    mode: str,
    expected_rank_seven_title: str,
) -> None:
    recommendations = recommend_songs(HIGH_ENERGY_POP, real_catalog, k=10, mode=mode)

    assert recommendations[6][0]["title"] == expected_rank_seven_title


def test_real_cli_energy_first_mode_exits_successfully() -> None:
    assert _run_cli("--mode", "energy-first", "--top-k", "3").returncode == 0


def test_real_cli_reports_the_energy_first_mode() -> None:
    assert "mode: energy-first" in _run_cli("--mode", "energy-first", "--top-k", "3").stdout


def test_real_cli_energy_first_reason_uses_the_energy_weight() -> None:
    assert "energy similarity 0.97:" in _run_cli(
        "--mode", "energy-first", "--top-k", "3"
    ).stdout


@pytest.fixture
def chill_lofi_top_five(real_catalog: list[SongRecord]) -> list[tuple[SongRecord, float, str]]:
    """Rank the checked-in catalog through the profile that demonstrates artist diversity."""
    return recommend_songs(USER_PROFILES["chill-lofi"], real_catalog, k=5)

@pytest.fixture
def focus_flow_recommendation(
    chill_lofi_top_five: list[tuple[SongRecord, float, str]],
) -> tuple[SongRecord, float, str]:
    """Provide Focus Flow's deterministic fifth-place diversity-adjusted result."""
    return chill_lofi_top_five[4]


def test_artist_diversity_penalty_reduces_a_repeated_artist_score(
    focus_flow_recommendation: tuple[SongRecord, float, str],
) -> None:
    unpenalized_score, _ = score_song(USER_PROFILES["chill-lofi"], focus_flow_recommendation[0])

    assert focus_flow_recommendation[1] < unpenalized_score


def test_artist_diversity_penalty_appears_in_the_reason(
    focus_flow_recommendation: tuple[SongRecord, float, str],
) -> None:
    assert "artist diversity penalty: -15.0 for 1 earlier selection(s)" in focus_flow_recommendation[2]


def test_real_cli_artist_diversity_profile_exits_successfully() -> None:
    assert _run_cli("--profile", "chill-lofi", "--top-k", "5").returncode == 0


def test_real_cli_explains_artist_diversity_penalty() -> None:
    assert "artist diversity penalty: -15.0 for 1 earlier selection(s)" in _run_cli(
        "--profile", "chill-lofi", "--top-k", "5"
    ).stdout
