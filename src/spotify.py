import os
import time
import json
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from dotenv import load_dotenv
from requests.exceptions import ConnectionError as RequestsConnectionError
from .chat import get_response
from .logger import get_logger

load_dotenv(override=True)

log = get_logger("spotify")

_VALID_MOODS = {"happy", "chill", "intense", "relaxed", "moody", "focused", "calm", "aggressive", "playful"}


def _client():
    return spotipy.Spotify(auth_manager=SpotifyClientCredentials(
        client_id=os.getenv("SPOTIFY_CLIENT_ID"),
        client_secret=os.getenv("SPOTIFY_CLIENT_SECRET"),
    ))


def _validate_prefs(prefs: dict) -> dict:
    """Clamp numeric prefs to valid ranges and fall back unknown moods to 'chill'."""
    safe = dict(prefs)
    safe["energy"] = max(0.0, min(1.0, float(safe.get("energy", 0.5))))
    safe["danceability"] = max(0.0, min(1.0, float(safe.get("danceability", 0.5))))
    safe["acousticness"] = max(0.0, min(1.0, float(safe.get("acousticness", 0.5))))
    safe["tempo"] = max(40, min(220, float(safe.get("tempo", 120))))
    if safe.get("mood") not in _VALID_MOODS:
        log.warning("Unknown mood '%s', defaulting to 'chill'", safe.get("mood"))
        safe["mood"] = "chill"
    return safe


def search_songs(genre: str, limit: int = 10) -> list:
    """Search Spotify by genre. Falls back to a plain keyword search if genre returns nothing."""
    limit = min(limit, 10)
    for attempt in range(3):
        try:
            sp = _client()
            log.info("Searching Spotify: genre='%s', limit=%d (attempt %d)", genre, limit, attempt + 1)
            results = sp.search(q=f"genre:{genre}", type="track", limit=limit)
            tracks = results["tracks"]["items"]

            if not tracks:
                log.warning("genre:'%s' returned 0 tracks, trying plain keyword search", genre)
                results = sp.search(q=genre, type="track", limit=limit)
                tracks = results["tracks"]["items"]

            log.info("Spotify returned %d tracks for '%s'", len(tracks), genre)
            return [
                {"title": t["name"], "artist": t["artists"][0]["name"], "genre": genre}
                for t in tracks
            ]
        except (RequestsConnectionError, spotipy.SpotifyException) as e:
            log.error("Spotify error on attempt %d: %s", attempt + 1, e)
            if attempt == 2:
                raise
            time.sleep(1.5 * (attempt + 1))
    return []


def rank_songs(prefs: dict, songs: list, k: int = 5) -> list:
    """Ask Groq to rank songs by how well they match the user's preferences. Returns top-k dicts."""
    if not songs:
        log.warning("rank_songs called with empty song list")
        return []

    prefs = _validate_prefs(prefs)

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
        log.info("Asking Groq to rank %d songs for prefs: %s", len(songs), prefs)
        response = get_response(messages)
        match = json.loads(response.strip())
        ranked = [songs[i - 1] for i in match if 1 <= i <= len(songs)]
        log.info("Groq ranked %d songs successfully", len(ranked))
        return ranked[:k]
    except Exception as e:
        log.error("Groq ranking failed: %s — returning unranked fallback", e)
        return songs[:k]
