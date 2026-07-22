"""Command-line runner for VibeFinder's explainable recommendation simulation."""

from __future__ import annotations

import argparse
from pathlib import Path
from textwrap import fill
from typing import Sequence

from tabulate import tabulate

from src.recommender import (
    STRATEGIES,
    get_strategy,
    load_songs,
    recommend_songs,
    score_song,
)

DEFAULT_PROFILE_NAME = "high-energy-pop"
DEFAULT_PROFILE = {
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
USER_PROFILES = {
    DEFAULT_PROFILE_NAME: DEFAULT_PROFILE,
    "chill-lofi": {
        "genre": "lofi",
        "mood": "chill",
        "energy": 0.30,
        "tempo_bpm": 80,
        "valence": 0.55,
        "danceability": 0.45,
        "likes_acoustic": True,
        "release_decade": 2000,
        "mood_tags": ("study", "warm"),
        "likes_instrumental": True,
        "liveness": 0.12,
        "speechiness": 0.05,
    },
    "deep-intense-rock": {
        "genre": "rock",
        "mood": "intense",
        "energy": 0.85,
        "tempo_bpm": 145,
        "valence": 0.40,
        "danceability": 0.55,
        "likes_acoustic": False,
        "release_decade": 1990,
        "mood_tags": ("guitar", "intense", "anthemic"),
        "likes_instrumental": False,
        "liveness": 0.15,
        "speechiness": 0.04,
    },
}
CATALOG_PATH = Path(__file__).resolve().parents[1] / "data" / "songs.csv"


def top_k_value(value: str) -> int:
    """Validate the CLI's catalog-sized top-k boundary."""
    top_k = int(value)
    if not 1 <= top_k <= 20:
        raise argparse.ArgumentTypeError("top-k must be between 1 and 20")
    return top_k


def build_parser() -> argparse.ArgumentParser:
    """Build the CLI interface for selecting profiles, modes, and top-k results."""
    parser = argparse.ArgumentParser(description="Rank VibeFinder's classroom music catalog.")
    parser.add_argument("--top-k", type=top_k_value, default=5, help="Number of recommendations (1–20).")
    parser.add_argument(
        "--profile",
        choices=USER_PROFILES,
        default=DEFAULT_PROFILE_NAME,
        help="Named taste profile to rank.",
    )
    parser.add_argument("--all-profiles", action="store_true", help="Run every named profile.")
    parser.add_argument(
        "--mode",
        choices=STRATEGIES,
        default="balanced",
        help="Ranking mode: balanced or energy-first.",
    )
    return parser


def render_recommendations(
    profile: dict[str, object], recommendations: list[tuple[dict[str, object], float, str]], mode: str
) -> str:
    """Render scores and their exact reasons in a readable terminal table."""
    strategy = get_strategy(mode)
    rows = []
    for rank, (song, final_score, explanation) in enumerate(recommendations, start=1):
        base_score, _ = score_song(profile, song, strategy=strategy)
        rows.append(
            [
                rank,
                song["title"],
                song["artist"],
                mode,
                f"{base_score:.2f}",
                f"{final_score:.2f}",
                fill(explanation, width=72),
            ]
        )
    return tabulate(
        rows,
        headers=["Rank", "Song", "Artist", "Mode", "Base score", "Final score", "Reasons"],
        tablefmt="rounded_outline",
        maxcolwidths=[None, 22, 22, 14, None, None, 72],
        stralign="left",
        numalign="right",
    )


def main(argv: Sequence[str] | None = None) -> None:
    """Load the real catalog, rank it, and print score-derived explanations."""
    args = build_parser().parse_args(argv)
    songs = load_songs(CATALOG_PATH)
    selected_profiles = USER_PROFILES.items() if args.all_profiles else [(args.profile, USER_PROFILES[args.profile])]
    for position, (profile_name, profile) in enumerate(selected_profiles):
        if position:
            print()
        recommendations = recommend_songs(profile, songs, args.top_k, args.mode)
        print(f"VibeFinder | profile: {profile_name} | mode: {args.mode}")
        print()
        print(render_recommendations(profile, recommendations, args.mode))


if __name__ == "__main__":
    main()
