from src.recommender import load_songs, recommend_songs

# Contrasting user profiles and their song histories (by song id)
contrasting_users = [
    {
        "prefs": {"genre": "pop", "mood": "happy", "energy": 0.8, "tempo": 120, "danceability": 0.8, "acousticness": 0.2},
        "history": [1, 5, 10, 13, 14]
    },
    {
        "prefs": {"genre": "metal", "mood": "aggressive", "energy": 0.95, "tempo": 160, "danceability": 0.55, "acousticness": 0.05},
        "history": [17, 3, 5, 8, 20]
    },
    {
        "prefs": {"genre": "classical", "mood": "calm", "energy": 0.3, "tempo": 90, "danceability": 0.45, "acousticness": 0.95},
        "history": [12, 4, 6, 18, 7]
    },
    {
        "prefs": {"genre": "reggae", "mood": "laid-back", "energy": 0.6, "tempo": 76, "danceability": 0.78, "acousticness": 0.5},
        "history": [19, 2, 6, 15, 9]
    },
    {
        "prefs": {"genre": "chiptune", "mood": "playful", "energy": 0.78, "tempo": 140, "danceability": 0.8, "acousticness": 0.12},
        "history": [13, 8, 20, 1, 14]
    },
]

# Similar user profiles and their song histories (by song id)
similar_users = [
    {
        "prefs": {"genre": "lofi", "mood": "chill", "energy": 0.4, "tempo": 80, "danceability": 0.6, "acousticness": 0.8},
        "history": [2, 4, 9, 6, 18]
    },
    {
        "prefs": {"genre": "lofi", "mood": "chill", "energy": 0.42, "tempo": 78, "danceability": 0.62, "acousticness": 0.71},
        "history": [2, 4, 9, 6, 18]
    },
    {
        "prefs": {"genre": "lofi", "mood": "chill", "energy": 0.35, "tempo": 72, "danceability": 0.58, "acousticness": 0.86},
        "history": [2, 4, 9, 6, 18]
    },
    {
        "prefs": {"genre": "lofi", "mood": "chill", "energy": 0.4, "tempo": 80, "danceability": 0.6, "acousticness": 0.8},
        "history": [2, 4, 9, 6, 18]
    },
    {
        "prefs": {"genre": "lofi", "mood": "chill", "energy": 0.42, "tempo": 78, "danceability": 0.62, "acousticness": 0.71},
        "history": [2, 4, 9, 6, 18]
    },
]

def test_contrasting_users_recommendations():
    songs = load_songs("data/songs.csv")
    for user in contrasting_users:
        results = recommend_songs(user["prefs"], songs, k=5)
        # Each user should get at least one song from their history in recommendations
        recommended_ids = [song.id for song, score, explanation in results]
        assert any(song_id in recommended_ids for song_id in user["history"])

def test_similar_users_recommendations():
    songs = load_songs("data/songs.csv")
    for user in similar_users:
        results = recommend_songs(user["prefs"], songs, k=5)
        recommended_ids = [song.id for song, score, explanation in results]
        # All similar users should have significant overlap in recommendations
        assert set(recommended_ids).intersection(set([2, 4, 9, 6, 18]))
from src.recommender import Song, UserProfile, Recommender

def make_small_recommender() -> Recommender:
    songs = [
        Song(
            id=1,
            title="Test Pop Track",
            artist="Test Artist",
            genre="pop",
            mood="happy",
            energy=0.8,
            tempo_bpm=120,
            danceability=0.8,
            acousticness=0.2,
        ),
        Song(
            id=2,
            title="Chill Lofi Loop",
            artist="Test Artist",
            genre="lofi",
            mood="chill",
            energy=0.4,
            tempo_bpm=80,
            danceability=0.5,
            acousticness=0.9,
        ),
    ]
    return Recommender(songs)


def test_recommend_returns_songs_sorted_by_score():
    user = UserProfile(
        favorite_genre="pop",
        favorite_mood="happy",
        target_energy=0.8,
        target_tempo=120,
        target_danceability=0.8,
        target_acousticness=0.2
    )
    rec = make_small_recommender()
    results = rec.recommend(user, k=2)

    assert len(results) == 2
    # Starter expectation: the pop, happy, high energy song should score higher
    assert results[0].genre == "pop"
    assert results[0].mood == "happy"


def test_explain_recommendation_returns_non_empty_string():
    user = UserProfile(
        favorite_genre="pop",
        favorite_mood="happy",
        target_energy=0.8,
        target_tempo=120,
        target_danceability=0.8,
        target_acousticness=0.2
    )
    rec = make_small_recommender()
    song = rec.songs[0]

    explanation = rec.explain_recommendation(user, song)
    assert isinstance(explanation, str)
    assert explanation.strip() != ""
