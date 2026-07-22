"""BDD coverage for VibeFinder's named profiles over its real catalog."""

from pytest_bdd import given, parsers, scenarios, then, when

from src.main import USER_PROFILES
from src.recommender import SongRecord, recommend_songs

scenarios("features/profile_recommendations.feature")

@given("the checked-in VibeFinder catalog", target_fixture="songs")
def checked_in_catalog(real_catalog: list[SongRecord]) -> list[SongRecord]:
    """Load the actual catalog used by the command-line application."""
    return real_catalog


@given(parsers.parse('the "{profile_name}" profile'), target_fixture="profile")
def named_profile(profile_name: str) -> SongRecord:
    """Select one real named profile rather than constructing test-only data."""
    return USER_PROFILES[profile_name]


@when("that profile requests three recommendations", target_fixture="recommendations")
def rank_named_profile(
    profile: SongRecord, songs: list[SongRecord]
) -> list[tuple[SongRecord, float, str]]:
    """Rank the checked-in data through the public functional API."""
    return recommend_songs(profile, songs, k=3)


@then("exactly three recommendations are returned")
def has_three_recommendations(recommendations: list[tuple[SongRecord, float, str]]) -> None:
    """Verify the requested top-k boundary."""
    assert len(recommendations) == 3


@then("recommendations are ordered from highest score to lowest score")
def is_descending(recommendations: list[tuple[SongRecord, float, str]]) -> None:
    """Verify the observable rank ordering."""
    assert recommendations[0][1] >= recommendations[1][1] >= recommendations[2][1]
