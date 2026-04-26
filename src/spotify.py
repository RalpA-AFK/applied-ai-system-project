import os
import time
import json
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from dotenv import load_dotenv
from requests.exceptions import ConnectionError as RequestsConnectionError
from .chat import get_response

load_dotenv(override=True)


def _client():
    return spotipy.Spotify(auth_manager=SpotifyClientCredentials(
        client_id=os.getenv("SPOTIFY_CLIENT_ID"),
        client_secret=os.getenv("SPOTIFY_CLIENT_SECRET"),
    ))


def search_songs(genre: str, limit: int = 10) -> list:
    """Search Spotify by genre and return a list of dicts with title, artist, and genre."""
    for attempt in range(3):
        try:
            sp = _client()
            results = sp.search(q=f"genre:{genre}", type="track", limit=min(limit, 10))
            tracks = results["tracks"]["items"]
            return [
                {"title": t["name"], "artist": t["artists"][0]["name"], "genre": genre}
                for t in tracks
            ]
        except (RequestsConnectionError, spotipy.SpotifyException):
            if attempt == 2:
                raise
            time.sleep(1.5 * (attempt + 1))
    return []


def rank_songs(prefs: dict, songs: list, k: int = 5) -> list:
    """Ask Groq to rank songs by how well they match the user's preferences. Returns top-k dicts."""
    if not songs:
        return []

    track_list = "\n".join(
        f"{i+1}. {s['title']} by {s['artist']}" for i, s in enumerate(songs)
    )
    mood = prefs.get("mood", "")
    genre = prefs.get("genre", "")
    energy_desc = "high energy" if prefs.get("energy", 0.5) > 0.6 else "low energy" if prefs.get("energy", 0.5) < 0.4 else "moderate energy"
    tempo_desc = "fast" if prefs.get("tempo", 120) > 130 else "slow" if prefs.get("tempo", 120) < 90 else "mid-tempo"

    messages = [
        {
            "role": "system",
            "content": "You are a music expert. Rank songs by how well they match a listener's preferences. Reply only with a JSON array of track numbers in order from best to worst match, e.g. [3,1,5,2,4].",
        },
        {
            "role": "user",
            "content": (
                f"Rank these {genre} tracks for someone who wants {mood}, {energy_desc}, {tempo_desc} music:\n\n"
                f"{track_list}\n\n"
                f"Reply with only a JSON array of the track numbers ranked best to worst."
            ),
        },
    ]

    try:
        response = get_response(messages)
        match = json.loads(response.strip())
        ranked = [songs[i - 1] for i in match if 1 <= i <= len(songs)]
        return ranked[:k]
    except Exception:
        return songs[:k]
