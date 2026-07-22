"""Command-line runner for VibeFinder's explainable recommendation simulation."""

from __future__ import annotations

import argparse
from pathlib import Path
from typing import Sequence

from src.recommender import load_songs, recommend_songs

DEFAULT_PROFILE_NAME = "high-energy-pop"
DEFAULT_PROFILE = {
    "genre": "pop",
    "mood": "happy",
    "energy": 0.85,
    "tempo_bpm": 130,
    "valence": 0.80,
    "danceability": 0.85,
    "likes_acoustic": False,
}
CATALOG_PATH = Path(__file__).resolve().parents[1] / "data" / "songs.csv"


def top_k_value(value: str) -> int:
    """Validate the CLI's catalog-sized top-k boundary."""
    top_k = int(value)
    if not 1 <= top_k <= 20:
        raise argparse.ArgumentTypeError("top-k must be between 1 and 20")
    return top_k


def build_parser() -> argparse.ArgumentParser:
    """Build the small CLI interface available before profile extensions."""
    parser = argparse.ArgumentParser(description="Rank VibeFinder's classroom music catalog.")
    parser.add_argument("--top-k", type=top_k_value, default=5, help="Number of recommendations (1–20).")
    parser.add_argument(
        "--mode",
        choices=["balanced"],
        default="balanced",
        help="Ranking mode; the energy-first extension adds another option.",
    )
    return parser


def main(argv: Sequence[str] | None = None) -> None:
    """Load the real catalog, rank it, and print score-derived explanations."""
    args = build_parser().parse_args(argv)
    recommendations = recommend_songs(DEFAULT_PROFILE, load_songs(CATALOG_PATH), args.top_k, args.mode)
    print(f"VibeFinder | profile: {DEFAULT_PROFILE_NAME} | mode: {args.mode}")
    print()
    for rank, (song, score, explanation) in enumerate(recommendations, start=1):
        print(f"{rank}. {song['title']} — {song['artist']} | {score:.2f}/100")
        print(f"   Why: {explanation}")


if __name__ == "__main__":
    main()
