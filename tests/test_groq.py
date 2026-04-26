import os
import pytest
from dotenv import load_dotenv

load_dotenv(override=True)

from src.spotify import search_songs, rank_songs


def test_groq_recommends_moody_slow_lofi():
    songs = search_songs("lo-fi", limit=10)
    assert len(songs) > 0, "No lo-fi tracks returned from Spotify"

    prefs = {"genre": "lo-fi", "mood": "moody", "energy": 0.3, "tempo": 75, "danceability": 0.4, "acousticness": 0.7}
    results = rank_songs(prefs, songs, k=5)

    assert len(results) > 0, "Groq returned no ranked results"
    assert all("title" in s and "artist" in s for s in results), "Results missing title or artist"

    titles = [s["title"].lower() for s in songs]
    assert any(r["title"].lower() in titles for r in results), "Ranked results contain unknown tracks"
