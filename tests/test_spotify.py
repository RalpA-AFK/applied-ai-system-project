import os
import pytest
from dotenv import load_dotenv

load_dotenv(override=True)

import spotipy
from spotipy.oauth2 import SpotifyClientCredentials


@pytest.fixture
def sp():
    return spotipy.Spotify(auth_manager=SpotifyClientCredentials(
        client_id=os.getenv("SPOTIFY_CLIENT_ID"),
        client_secret=os.getenv("SPOTIFY_CLIENT_SECRET"),
    ))


def test_my_way_frank_sinatra(sp):
    results = sp.search(q="My Way Frank Sinatra", type="track", limit=10)
    tracks = results["tracks"]["items"]

    assert len(tracks) > 0, "No tracks returned from Spotify"

    titles = [t["name"].lower() for t in tracks]
    artists = [t["artists"][0]["name"].lower() for t in tracks]

    assert any("my way" in title for title in titles), "My Way not found in results"
    assert any("sinatra" in artist for artist in artists), "Frank Sinatra not found in results"
