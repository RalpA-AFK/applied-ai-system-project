# Music Recommender

A conversational music recommendation app. You chat with an AI that learns your taste, searches Spotify for real tracks, and ranks them for you — all running in your browser on localhost.

---

## How It Works

1. **Chat** — A Groq-powered AI (Llama 3) asks you a few questions about your mood, genre preferences, energy level, and tempo
2. **Search** — Once it understands your taste, it searches the Spotify API for real tracks matching your genre
3. **Rank** — Groq reads the results and ranks them by how well they fit what you described
4. **Display** — The top picks are shown in a clean web UI

```
You (chat)
    │
    ▼
Groq / Llama 3 (conversation + ranking)
    │
    ▼
Spotify Web API (track search)
    │
    ▼
Ranked recommendations shown in browser
```

---

## Setup

### 1. Clone the repo

```bash
git clone <your-repo-url>
cd applied-ai-system-project
```

### 2. Create a virtual environment

```bash
python -m venv .venv
source .venv/bin/activate      # Mac / Linux
.venv\Scripts\activate         # Windows
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Set up your API keys

Copy the example env file and fill in your keys:

```bash
cp .env.example .env
```

Then open `.env` and add your credentials (see the sections below for how to get them).

---

## Getting a Groq API Key

Groq provides free access to Llama 3 with no credit card required.

1. Go to [console.groq.com](https://console.groq.com) and sign up
2. Navigate to **API Keys** in the left sidebar
3. Click **Create API Key**
4. Copy the key and paste it into your `.env` file:

```
GROQ_API_KEY=your_key_here
```

---

## Getting Spotify API Credentials

Spotify's Web API is free for non-commercial use.

1. Go to [developer.spotify.com/dashboard](https://developer.spotify.com/dashboard) and log in with your Spotify account
2. Click **Create App**
3. Fill in any name and description
4. Set the Redirect URI to `http://localhost:8888/callback`
5. Click **Save**
6. On your app's page, click **Settings** to find your **Client ID** and **Client Secret**
7. Copy both into your `.env` file:

```
SPOTIFY_CLIENT_ID=your_client_id_here
SPOTIFY_CLIENT_SECRET=your_client_secret_here
```

> Note: New Spotify apps start in Development mode, which limits search results to 10 tracks per request. This is enough for the app to work.

---

## Running the App

```bash
python -m streamlit run app.py
```

The app will open automatically at `http://localhost:8501`.

---

## Running Tests

```bash
python -m pytest -v
```

The test suite covers:
- In-memory scoring logic (`tests/test_recommender.py`)
- Spotify search integration (`tests/test_spotify.py`)
- Groq ranking integration (`tests/test_groq.py`)

---

## Project Structure

```
app.py                  # Streamlit web app (entry point)
src/
  chat.py               # Groq conversation logic
  spotify.py            # Spotify search and Groq-based ranking
  recommender.py        # Song and UserProfile data models, scoring logic
  main.py               # Terminal entry point (alternative to app.py)
tests/
  test_recommender.py   # Unit tests for scoring logic
  test_spotify.py       # Integration tests for Spotify API
  test_groq.py          # Integration tests for Groq ranking
.env.example            # Template for required environment variables
```
