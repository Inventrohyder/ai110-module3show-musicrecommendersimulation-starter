"""Shared real-data fixtures for VibeFinder's integration and BDD tests."""

from pathlib import Path

import pytest

from src.recommender import SongRecord, load_songs

CATALOG_PATH = Path(__file__).parents[1] / "data" / "songs.csv"


@pytest.fixture
def real_catalog() -> list[SongRecord]:
    """Provide a fresh copy of the checked-in catalog for each test scenario."""
    return load_songs(CATALOG_PATH)
