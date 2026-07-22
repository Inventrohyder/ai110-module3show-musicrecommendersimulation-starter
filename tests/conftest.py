"""Shared real-data fixtures for VibeFinder's integration and BDD tests."""

import subprocess
import sys
from collections.abc import Callable
from pathlib import Path

import pytest

from src.recommender import SongRecord, load_songs

CATALOG_PATH = Path(__file__).parents[1] / "data" / "songs.csv"
PROJECT_ROOT = Path(__file__).parents[1]


@pytest.fixture
def real_catalog() -> list[SongRecord]:
    """Provide a fresh copy of the checked-in catalog for each test scenario."""
    return load_songs(CATALOG_PATH)


@pytest.fixture
def run_cli() -> Callable[..., subprocess.CompletedProcess[str]]:
    """Run the actual command-line application from the project root."""

    def invoke(*arguments: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, "-m", "src.main", *arguments],
            cwd=PROJECT_ROOT,
            capture_output=True,
            check=False,
            text=True,
        )

    return invoke
