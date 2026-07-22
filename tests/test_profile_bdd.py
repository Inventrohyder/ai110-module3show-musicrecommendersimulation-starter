"""End-to-end BDD coverage for VibeFinder's named-profile CLI journeys."""

import re
import subprocess
from collections.abc import Callable

from pytest_bdd import parsers, scenarios, then, when

scenarios("features/profile_recommendations.feature")

CliRunner = Callable[..., subprocess.CompletedProcess[str]]


@when(
    parsers.parse('I run the VibeFinder CLI for the "{profile_name}" profile'),
    target_fixture="cli_result",
)
def run_named_profile_cli(
    run_cli: CliRunner,
    profile_name: str,
) -> subprocess.CompletedProcess[str]:
    """Exercise the actual command-line entry point for one named listener."""
    return run_cli("--profile", profile_name, "--top-k", "3")


@then("the CLI exits successfully")
def cli_exits_successfully(cli_result: subprocess.CompletedProcess[str]) -> None:
    """Verify that the user-facing command completed successfully."""
    assert cli_result.returncode == 0


@then(parsers.parse('the output identifies the "{profile_name}" profile'))
def output_identifies_profile(cli_result: subprocess.CompletedProcess[str], profile_name: str) -> None:
    """Verify the profile label shown to a CLI user."""
    assert f"profile: {profile_name}" in cli_result.stdout


@then(parsers.parse('the first table recommendation is "{song_title}"'))
def output_includes_first_table_recommendation(
    cli_result: subprocess.CompletedProcess[str],
    song_title: str,
) -> None:
    """Verify the first rendered table row without constructing a test-only result."""
    assert re.search(rf"│\s*1\s*│\s*{re.escape(song_title)}\s*│", cli_result.stdout)


@then(parsers.parse('the table shows the "{reason_fragment}" contribution'))
def output_includes_score_reason(
    cli_result: subprocess.CompletedProcess[str],
    reason_fragment: str,
) -> None:
    """Verify that the actual table exposes a score-derived reason."""
    assert reason_fragment in cli_result.stdout
