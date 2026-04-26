import os
import json
import re
from groq import Groq
from dotenv import load_dotenv

load_dotenv(override=True)

SYSTEM_PROMPT = """You are a friendly music taste assistant. Chat naturally with the user to learn what kind of music they want right now. Ask 3-4 short, conversational questions covering:
- Genre (e.g. pop, rock, jazz, lo-fi, hip hop, classical, metal, reggae)
- Mood (choose from: happy, chill, intense, relaxed, moody, focused, calm, aggressive, playful)
- Energy level (0.0 = very calm, 1.0 = very energetic)
- Tempo (slow ~80 BPM, medium ~120 BPM, fast ~160 BPM)
- Danceability (0.0 = not danceable, 1.0 = very danceable)
- Acousticness (0.0 = fully electronic, 1.0 = fully acoustic)

Once you have gathered enough information, output ONLY a JSON block with no extra text after it:
```json
{
  "genre": "pop",
  "mood": "happy",
  "energy": 0.8,
  "tempo": 120,
  "danceability": 0.7,
  "acousticness": 0.2
}
```"""


def get_response(messages: list) -> str:
    """Send a message list to Groq and return the response text."""
    client = Groq(api_key=os.getenv("GROQ_API_KEY"))
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=messages,
    )
    return response.choices[0].message.content


def stream_response(messages: list):
    """Yield response chunks from Groq. Pass directly to st.write_stream."""
    client = Groq(api_key=os.getenv("GROQ_API_KEY"))
    stream = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=messages,
        stream=True,
    )
    for chunk in stream:
        content = chunk.choices[0].delta.content
        if content:
            yield content


def extract_prefs(text: str) -> dict | None:
    """Parse a JSON prefs block from the model response. Returns None if not found."""
    match = re.search(r"```json\s*(\{.*?\})\s*```", text, re.DOTALL)
    if match:
        return json.loads(match.group(1))
    return None


def run_chat() -> dict:
    """Terminal chat loop. Returns prefs dict when complete."""
    messages = [{"role": "system", "content": SYSTEM_PROMPT}]

    print("\n--- Music Recommender ---\n")
    messages.append({"role": "user", "content": "Start with a friendly opening question."})
    opening = get_response(messages)
    messages.append({"role": "assistant", "content": opening})
    print(f"Assistant: {opening}\n")

    while True:
        user_input = input("You: ").strip()
        if not user_input:
            continue
        messages.append({"role": "user", "content": user_input})
        text = get_response(messages)
        messages.append({"role": "assistant", "content": text})

        prefs = extract_prefs(text)
        if prefs:
            print("\nGot it! Searching Spotify...\n")
            return prefs
        print(f"\nAssistant: {text}\n")
