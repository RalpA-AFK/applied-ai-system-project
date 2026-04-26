"""
Evaluation harness — runs predefined scenarios through the full pipeline
and prints a pass/fail summary with confidence scores.

Run with:
    python tests/eval.py
"""

import os
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

# Allow Unicode output on Windows terminals
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

from dotenv import load_dotenv
load_dotenv(override=True)

from src.spotify import search_songs, rank_songs

SCENARIOS = [
    {
        "name": "Chill lo-fi study session",
        "prefs": {
            "genre": "lo-fi", "mood": "chill",
            "energy": 0.3, "tempo": 80, "danceability": 0.4, "acousticness": 0.8,
        },
    },
    {
        "name": "High energy hip hop workout",
        "prefs": {
            "genre": "hip-hop", "mood": "intense",
            "energy": 0.9, "tempo": 150, "danceability": 0.85, "acousticness": 0.1,
        },
    },
    {
        "name": "Moody jazz rainy afternoon",
        "prefs": {
            "genre": "jazz", "mood": "moody",
            "energy": 0.35, "tempo": 85, "danceability": 0.4, "acousticness": 0.7,
        },
    },
]


def _confidence(results: list, songs: list) -> float:
    """Simple confidence score: fraction of ranked results that came from the original search."""
    if not results or not songs:
        return 0.0
    original_titles = {s["title"].lower() for s in songs}
    matched = sum(1 for r in results if r["title"].lower() in original_titles)
    return matched / len(results)


def run_eval():
    passed = 0
    failed = 0
    total_confidence = 0.0

    print("\n=== Music Recommender — Evaluation Harness ===\n")

    for scenario in SCENARIOS:
        name = scenario["name"]
        prefs = scenario["prefs"]
        genre = prefs["genre"]
        print(f"Scenario : {name}")
        print(f"Prefs    : genre={genre}, mood={prefs['mood']}, energy={prefs['energy']}, tempo={prefs['tempo']}")

        try:
            songs = search_songs(genre, limit=10)
            if not songs:
                print(f"Result   : FAIL — Spotify returned 0 tracks for '{genre}'\n")
                failed += 1
                continue

            results = rank_songs(prefs, songs, k=5)

            if not results:
                print(f"Result   : FAIL — Groq returned 0 ranked results\n")
                failed += 1
                continue

            if not all("title" in r and "artist" in r for r in results):
                print(f"Result   : FAIL — Results missing required fields\n")
                failed += 1
                continue

            conf = _confidence(results, songs)
            print(f"Result   : PASS ({len(results)} results, confidence {conf:.0%})")
            for i, r in enumerate(results, 1):
                print(f"  {i}. {r['title']} - {r['artist']}")
            print()
            passed += 1
            total_confidence += conf

        except Exception as e:
            print(f"Result   : FAIL — {e}\n")
            failed += 1

        time.sleep(0.5)

    total = passed + failed
    avg_conf = total_confidence / passed if passed else 0.0
    print("=" * 48)
    print(f"Passed          : {passed}/{total}")
    print(f"Avg confidence  : {avg_conf:.0%}")
    print("=" * 48 + "\n")


if __name__ == "__main__":
    run_eval()
