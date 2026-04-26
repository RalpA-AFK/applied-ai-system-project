"""
Entry point for the Music Recommender App.

Run with:
    python -m src.main
"""

from dotenv import load_dotenv
load_dotenv(override=True)

from .chat import run_chat
from .spotify import search_songs, rank_songs


def main() -> None:
    prefs = run_chat()
    genre = prefs.get("genre", "pop")

    songs = search_songs(genre, limit=10)
    if not songs:
        print(f"No Spotify results found for '{genre}'. Try a different genre.")
        return

    results = rank_songs(prefs, songs, k=5)

    print("Top picks for you:\n")
    for i, song in enumerate(results, 1):
        print(f"  {i}. {song['title']} — {song['artist']}")
    print()


if __name__ == "__main__":
    main()
