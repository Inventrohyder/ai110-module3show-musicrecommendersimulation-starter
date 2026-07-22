"""Behavior-focused tests over VibeFinder's checked-in catalog and real CLI."""

import subprocess
from collections.abc import Callable
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

MALFORMED_CATALOG_PATH = Path(__file__).parent / "fixtures" / "malformed_songs.csv"
CliRunner = Callable[..., subprocess.CompletedProcess[str]]
Recommendation = tuple[SongRecord, float, str]
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
def happy_song(real_catalog: list[SongRecord]) -> SongRecord:
    """Provide the checked-in MusicBrainz-verified Happy row for score experiments."""
    return real_catalog[10]


@pytest.fixture
def high_energy_pop_top_three(real_catalog: list[SongRecord]) -> list[Recommendation]:
    """Rank the real catalog for the default high-energy pop scenario."""
    return recommend_songs(HIGH_ENERGY_POP, real_catalog, k=3)


@pytest.fixture
def oop_parity_case(real_catalog: list[SongRecord]) -> tuple[UserProfile, Recommendation, Song]:
    """Run the functional and OOP public APIs against the same checked-in catalog."""
    user = UserProfile(
        favorite_genre="pop",
        favorite_mood="happy",
        target_energy=0.85,
        likes_acoustic=False,
        target_tempo=130,
        target_valence=0.80,
        target_danceability=0.85,
    )
    functional_top = recommend_songs(user.to_preferences(), real_catalog, k=3)[0]
    object_top = Recommender([Song.from_record(song) for song in real_catalog]).recommend(user, k=3)[0]

    return user, functional_top, object_top


def test_checked_in_catalog_has_twenty_rows(real_catalog: list[SongRecord]) -> None:
    assert len(real_catalog) == 20


def test_checked_in_catalog_preserves_the_first_starter_song(real_catalog: list[SongRecord]) -> None:
    assert real_catalog[0]["title"] == "Sunrise City"


def test_checked_in_catalog_has_unique_song_ids(real_catalog: list[SongRecord]) -> None:
    assert len({song["id"] for song in real_catalog}) == len(real_catalog)


def test_functional_recommendations_return_the_requested_count(
    high_energy_pop_top_three: list[Recommendation],
) -> None:
    assert len(high_energy_pop_top_three) == 3


def test_functional_recommendations_are_descending(
    high_energy_pop_top_three: list[Recommendation],
) -> None:
    assert high_energy_pop_top_three[0][1] >= high_energy_pop_top_three[1][1] >= high_energy_pop_top_three[2][1]


def test_functional_recommendations_match_the_profile_genre(
    high_energy_pop_top_three: list[Recommendation],
) -> None:
    assert high_energy_pop_top_three[0][0]["genre"] == "pop"


def test_functional_recommendation_reason_includes_energy_contribution(
    high_energy_pop_top_three: list[Recommendation],
) -> None:
    assert "energy similarity" in high_energy_pop_top_three[0][2]


def test_functional_recommendation_reason_includes_acoustic_contribution(
    high_energy_pop_top_three: list[Recommendation],
) -> None:
    assert "acoustic preference" in high_energy_pop_top_three[0][2]


def test_oop_wrapper_matches_the_functional_top_recommendation(
    oop_parity_case: tuple[UserProfile, Recommendation, Song],
) -> None:
    _, functional_top, object_top = oop_parity_case

    assert object_top.id == functional_top[0]["id"]


def test_oop_wrapper_matches_the_functional_explanation(
    oop_parity_case: tuple[UserProfile, Recommendation, Song],
) -> None:
    user, functional_top, object_top = oop_parity_case

    assert Recommender([object_top]).explain_recommendation(user, object_top) == functional_top[2]


def test_malformed_checked_in_catalog_reports_the_boundary_problem() -> None:
    with pytest.raises(ValueError, match="energy must be between 0 and 1"):
        load_songs(MALFORMED_CATALOG_PATH)


def test_real_song_score_is_positive(real_catalog: list[SongRecord]) -> None:
    score, _ = score_song(HIGH_ENERGY_POP, real_catalog[0])

    assert score > 0


def test_real_song_score_explanation_includes_energy(real_catalog: list[SongRecord]) -> None:
    _, reasons = score_song(HIGH_ENERGY_POP, real_catalog[0])

    assert "energy similarity" in reasons[2]


@pytest.fixture
def default_cli_result(run_cli: CliRunner) -> subprocess.CompletedProcess[str]:
    """Run the default user-facing command with three requested results."""
    return run_cli("--top-k", "3")


@pytest.fixture
def invalid_top_k_cli_result(run_cli: CliRunner) -> subprocess.CompletedProcess[str]:
    """Run the public CLI with an invalid top-k boundary value."""
    return run_cli("--top-k", "21")


@pytest.fixture
def all_profiles_cli_result(run_cli: CliRunner) -> subprocess.CompletedProcess[str]:
    """Run every supported named profile through the real CLI."""
    return run_cli("--all-profiles", "--top-k", "3")


def test_real_cli_default_profile_exits_successfully(default_cli_result: subprocess.CompletedProcess[str]) -> None:
    assert default_cli_result.returncode == 0


def test_real_cli_default_profile_includes_the_transparent_table_columns(
    default_cli_result: subprocess.CompletedProcess[str],
) -> None:
    assert "Base score" in default_cli_result.stdout


def test_real_cli_default_profile_identifies_its_profile_and_mode(
    default_cli_result: subprocess.CompletedProcess[str],
) -> None:
    assert "VibeFinder | profile: high-energy-pop | mode: balanced" in default_cli_result.stdout


def test_real_cli_default_profile_has_the_expected_first_recommendation(
    default_cli_result: subprocess.CompletedProcess[str],
) -> None:
    assert "Sunrise City" in default_cli_result.stdout


def test_real_cli_default_profile_explains_the_first_recommendation(
    default_cli_result: subprocess.CompletedProcess[str],
) -> None:
    assert "genre match: +18.0/18" in default_cli_result.stdout


def test_real_cli_rejects_an_out_of_range_top_k_with_a_nonzero_status(
    invalid_top_k_cli_result: subprocess.CompletedProcess[str],
) -> None:
    assert invalid_top_k_cli_result.returncode != 0


def test_real_cli_rejects_an_out_of_range_top_k_with_a_clear_error(
    invalid_top_k_cli_result: subprocess.CompletedProcess[str],
) -> None:
    assert "top-k must be between 1 and 20" in invalid_top_k_cli_result.stderr


@pytest.mark.parametrize(
    "profile_name",
    (
        pytest.param("high-energy-pop", id="high-energy-pop"),
        pytest.param("chill-lofi", id="chill-lofi"),
        pytest.param("deep-intense-rock", id="deep-intense-rock"),
    ),
)
@pytest.mark.parametrize(
    "recommendation_index",
    (
        pytest.param(0, id="rank-1"),
        pytest.param(1, id="rank-2"),
        pytest.param(2, id="rank-3"),
    ),
)
@pytest.mark.parametrize(
    "reason_fragment",
    (
        pytest.param("genre", id="genre-reason"),
        pytest.param("energy", id="energy-reason"),
    ),
)
def test_each_named_profile_recommendation_exposes_a_score_derived_reason(
    real_catalog: list[SongRecord],
    profile_name: str,
    recommendation_index: int,
    reason_fragment: str,
) -> None:
    recommendations = recommend_songs(USER_PROFILES[profile_name], real_catalog, k=3)

    assert reason_fragment in recommendations[recommendation_index][2]


def test_energy_removal_experiment_changes_a_verified_song_score(happy_song: SongRecord) -> None:
    with_energy, _ = score_song(HIGH_ENERGY_POP, happy_song)
    without_energy, _ = score_song(HIGH_ENERGY_POP, happy_song, include_energy=False)

    assert with_energy != without_energy


def test_energy_removal_experiment_explains_the_excluded_feature(happy_song: SongRecord) -> None:
    _, reasons = score_song(HIGH_ENERGY_POP, happy_song, include_energy=False)

    assert "energy excluded for experiment" in reasons[2]


def test_advanced_release_decade_preference_changes_a_verified_song_score(
    happy_song: SongRecord,
) -> None:
    matching_score, _ = score_song(HIGH_ENERGY_POP, happy_song)
    earlier_era = {**HIGH_ENERGY_POP, "release_decade": 1950}
    earlier_score, _ = score_song(earlier_era, happy_song)

    assert matching_score > earlier_score


def test_advanced_release_decade_preference_appears_in_its_reason(
    happy_song: SongRecord,
) -> None:
    _, reasons = score_song(HIGH_ENERGY_POP, happy_song)

    assert "release decade similarity 1.00" in reasons[7]


def test_advanced_mood_tags_appear_in_their_reason(happy_song: SongRecord) -> None:
    _, reasons = score_song(HIGH_ENERGY_POP, happy_song)

    assert "mood-tag overlap" in reasons[8]


def test_real_cli_runs_all_named_profiles_successfully(
    all_profiles_cli_result: subprocess.CompletedProcess[str],
) -> None:
    assert all_profiles_cli_result.returncode == 0


@pytest.mark.parametrize(
    "profile_name",
    (
        pytest.param("high-energy-pop", id="all-profiles-includes-high-energy-pop"),
        pytest.param("chill-lofi", id="all-profiles-includes-chill-lofi"),
        pytest.param("deep-intense-rock", id="all-profiles-includes-deep-intense-rock"),
    ),
)
def test_real_cli_includes_each_named_profile(
    all_profiles_cli_result: subprocess.CompletedProcess[str],
    profile_name: str,
) -> None:
    assert f"profile: {profile_name}" in all_profiles_cli_result.stdout


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


@pytest.fixture
def energy_first_cli_result(run_cli: CliRunner) -> subprocess.CompletedProcess[str]:
    """Run the real CLI with the energy-first strategy."""
    return run_cli("--mode", "energy-first", "--top-k", "3")


def test_real_cli_energy_first_mode_exits_successfully(
    energy_first_cli_result: subprocess.CompletedProcess[str],
) -> None:
    assert energy_first_cli_result.returncode == 0


def test_real_cli_reports_the_energy_first_mode(
    energy_first_cli_result: subprocess.CompletedProcess[str],
) -> None:
    assert "mode: energy-first" in energy_first_cli_result.stdout


def test_real_cli_energy_first_reason_uses_the_energy_weight(
    energy_first_cli_result: subprocess.CompletedProcess[str],
) -> None:
    assert "energy similarity 0.97:" in energy_first_cli_result.stdout


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


@pytest.fixture
def chill_lofi_cli_result(run_cli: CliRunner) -> subprocess.CompletedProcess[str]:
    """Run the real CLI through the profile that exposes the artist penalty."""
    return run_cli("--profile", "chill-lofi", "--top-k", "5")


def test_artist_diversity_penalty_reduces_a_repeated_artist_score(
    focus_flow_recommendation: tuple[SongRecord, float, str],
) -> None:
    unpenalized_score, _ = score_song(USER_PROFILES["chill-lofi"], focus_flow_recommendation[0])

    assert focus_flow_recommendation[1] < unpenalized_score


def test_artist_diversity_penalty_appears_in_the_reason(
    focus_flow_recommendation: tuple[SongRecord, float, str],
) -> None:
    assert "artist diversity penalty: -15.0 for 1 earlier selection(s)" in focus_flow_recommendation[2]


def test_real_cli_artist_diversity_profile_exits_successfully(
    chill_lofi_cli_result: subprocess.CompletedProcess[str],
) -> None:
    assert chill_lofi_cli_result.returncode == 0


def test_real_cli_explains_artist_diversity_penalty(
    chill_lofi_cli_result: subprocess.CompletedProcess[str],
) -> None:
    assert "artist diversity penalty: -15.0 for 1 earlier selection(s)" in chill_lofi_cli_result.stdout
