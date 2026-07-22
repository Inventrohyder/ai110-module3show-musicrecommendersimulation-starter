"""BDD coverage for VibeFinder's named profiles over its real catalog."""

from pathlib import Path

from pytest_bdd import given, parsers, scenarios, then, when

from src.main import USER_PROFILES
from src.recommender import load_songs, recommend_songs

scenarios("features/profile_recommendations.feature")

CATALOG_PATH = Path(__file__).parents[1] / "data" / "songs.csv"


@given("the checked-in VibeFinder catalog", target_fixture="songs")
def checked_in_catalog() -> list[dict[str, object]]:
    """Load the actual catalog used by the command-line application."""
    return load_songs(CATALOG_PATH)


@given(parsers.parse('the "{profile_name}" profile'), target_fixture="profile")
def named_profile(profile_name: str) -> dict[str, object]:
    """Select one real named profile rather than constructing test-only data."""
    return USER_PROFILES[profile_name]


@when("that profile requests three recommendations", target_fixture="recommendations")
def rank_named_profile(
    profile: dict[str, object], songs: list[dict[str, object]]
) -> list[tuple[dict[str, object], float, str]]:
    """Rank the checked-in data through the public functional API."""
    return recommend_songs(profile, songs, k=3)


@then("exactly three recommendations are returned")
def has_three_recommendations(recommendations: list[tuple[dict[str, object], float, str]]) -> None:
    """Verify the requested top-k boundary."""
    assert len(recommendations) == 3


@then("recommendations are ordered from highest score to lowest score")
def is_descending(recommendations: list[tuple[dict[str, object], float, str]]) -> None:
    """Verify the observable rank ordering."""
    assert [score for _, score, _ in recommendations] == sorted(
        (score for _, score, _ in recommendations), reverse=True
    )


@then("every returned recommendation has score-derived reasons")
def has_score_derived_reasons(recommendations: list[tuple[dict[str, object], float, str]]) -> None:
    """Verify that explanations expose the scorer's contributions."""
    assert all("genre" in explanation and "energy" in explanation for _, _, explanation in recommendations)
