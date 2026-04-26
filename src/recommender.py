from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass

@dataclass
class Song:
    """
    Represents a song and its attributes.
    Required by tests/test_recommender.py
    """
    id: int
    title: str
    artist: str
    genre: str
    mood: str
    energy: float
    tempo_bpm: float
    # valence removed as per user request
    danceability: float
    acousticness: float

@dataclass
class UserProfile:
    """
    Represents a user's taste preferences.
    Required by tests/test_recommender.py
    """
    favorite_genre: str
    favorite_mood: str
    target_energy: float
    target_tempo: float
    target_danceability: float
    target_acousticness: float

class Recommender:
    """
    OOP implementation of the recommendation logic.
    Required by tests/test_recommender.py
    """
    def __init__(self, songs: List[Song]):
        """Initialize the recommender with a list of songs."""
        self.songs = songs

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        """Recommend top-k songs for a user profile."""
        # Content-based scoring system
        scored = []
        for song in self.songs:
            score = score_song(song, user)
            if score >= 0.85:
                scored.append((song, score))
        scored.sort(key=lambda x: x[1], reverse=True)
        return [s for s, _ in scored[:k]]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        """Generate explanation for a song recommendation."""
        # Simple explanation
        explanation = []
        if song.genre == user.favorite_genre:
            explanation.append("Genre match")
        if song.mood == user.favorite_mood:
            explanation.append("Mood match")
        if abs(song.energy - user.target_energy) < 0.15:
            explanation.append("Energy close to preference")
        if abs(song.tempo_bpm - user.target_tempo) < 10:
            explanation.append("Tempo close to preference")
        if abs(song.danceability - user.target_danceability) < 0.2:
            explanation.append("Danceability close to preference")
        if abs(song.acousticness - user.target_acousticness) < 0.2:
            explanation.append("Acousticness close to preference")
        return ", ".join(explanation) if explanation else "No strong match"


def score_song(song: Song, user: UserProfile) -> float:
    """Score a song for a given user profile."""
    """
    Scores a song for a user based on agreed weights and thresholds.
    """
    score = 0.0
    # Weights
    weights = {
        'mood': 0.24,
        'tempo': 0.19,
        'energy': 0.19,
        'genre': 0.14,
        'danceability': 0.14,
        'acousticness': 0.05,
        'title': 0.025,
        'artist': 0.025
    }
    # Mood
    if song.mood == user.favorite_mood:
        score += weights['mood']
    # Tempo (linear scale within 10 BPM)
    tempo_diff = abs(song.tempo_bpm - user.target_tempo)
    if tempo_diff < 10:
        score += weights['tempo'] * (1 - tempo_diff / 10)
    # Energy (linear scale within 0.15)
    energy_diff = abs(song.energy - user.target_energy)
    if energy_diff < 0.15:
        score += weights['energy'] * (1 - energy_diff / 0.15)
    # Genre
    if song.genre == user.favorite_genre:
        score += weights['genre']
    # Danceability (linear scale within 0.2)
    dance_diff = abs(song.danceability - user.target_danceability)
    if dance_diff < 0.2:
        score += weights['danceability'] * (1 - dance_diff / 0.2)
    # Acousticness (linear scale within 0.2)
    acoustic_diff = abs(song.acousticness - user.target_acousticness)
    if acoustic_diff < 0.2:
        score += weights['acousticness'] * (1 - acoustic_diff / 0.2)
    # Title (exact match, very low weight)
    if hasattr(user, 'favorite_title') and song.title == getattr(user, 'favorite_title', None):
        score += weights['title']
    # Artist (exact match, very low weight)
    if hasattr(user, 'favorite_artist') and song.artist == getattr(user, 'favorite_artist', None):
        score += weights['artist']
    return score

def recommend_songs(user_prefs: Dict, songs: List[Song], k: int = 5) -> List[Tuple[Song, float, str]]:
    """Recommend top-k songs with scores and explanations."""
    """
    Functional implementation of the recommendation logic.
    Required by src/main.py
    """
    # Expected return format: (song_dict, score, explanation)
    user = UserProfile(
        favorite_genre=user_prefs.get('genre', ''),
        favorite_mood=user_prefs.get('mood', ''),
        target_energy=user_prefs.get('energy', 0.5),
        target_tempo=user_prefs.get('tempo', 120),
        target_danceability=user_prefs.get('danceability', 0.5),
        target_acousticness=user_prefs.get('acousticness', 0.5)
    )
    results = []
    for song in songs:
        score = score_song(song, user)
        if score >= 0.85:
            explanation = f"Score: {score:.2f} - "
            if song.genre == user.favorite_genre:
                explanation += "Genre match, "
            if song.mood == user.favorite_mood:
                explanation += "Mood match, "
            if abs(song.energy - user.target_energy) < 0.15:
                explanation += "Energy close, "
            if abs(song.tempo_bpm - user.target_tempo) < 10:
                explanation += "Tempo close, "
            if abs(song.danceability - user.target_danceability) < 0.2:
                explanation += "Danceability close, "
            if abs(song.acousticness - user.target_acousticness) < 0.2:
                explanation += "Acousticness close, "
            results.append((song, score, explanation.strip(', ')))
    results.sort(key=lambda x: x[1], reverse=True)
    return results[:k]
