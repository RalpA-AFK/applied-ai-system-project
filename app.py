import re
import streamlit as st
from dotenv import load_dotenv

load_dotenv(override=True)

from src.chat import SYSTEM_PROMPT, stream_response, extract_prefs
from src.spotify import search_songs, rank_songs
from src.logger import get_logger

log = get_logger("app")

st.set_page_config(page_title="Music Recommender", layout="centered")
st.title("Music Recommender")

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "system", "content": SYSTEM_PROMPT}]
    st.session_state.prefs = None
    st.session_state.recommendations = None
    log.info("New session started")

# Render existing chat history
for msg in st.session_state.messages:
    if msg["role"] == "system":
        continue
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# Stream opening message on first load
if not any(m["role"] == "assistant" for m in st.session_state.messages):
    with st.chat_message("assistant"):
        init_msgs = st.session_state.messages + [
            {"role": "user", "content": "Start with a friendly opening question."}
        ]
        opening = st.write_stream(stream_response(init_msgs))
    st.session_state.messages.append({"role": "assistant", "content": opening})
    log.info("Opening message streamed")
    st.rerun()

# Show recommendations
elif st.session_state.recommendations:
    st.divider()
    st.subheader("Top Picks For You")
    for i, song in enumerate(st.session_state.recommendations, 1):
        st.markdown(f"**{i}. {song['title']}** — {song['artist']}")
    if st.button("Start Over"):
        log.info("User started a new session")
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.rerun()

# Search Spotify once prefs are captured
elif st.session_state.prefs is not None:
    genre = st.session_state.prefs.get("genre", "pop")
    with st.spinner("Searching Spotify for your tracks..."):
        try:
            songs = search_songs(genre, limit=10)
            if not songs:
                log.warning("Spotify returned no songs for genre '%s'", genre)
                st.warning(f"Couldn't find any tracks for **{genre}** on Spotify. Try starting over with a different genre.")
                if st.button("Start Over"):
                    for key in list(st.session_state.keys()):
                        del st.session_state[key]
                    st.rerun()
            else:
                st.session_state.recommendations = rank_songs(st.session_state.prefs, songs, k=5)
                st.rerun()
        except ConnectionError:
            log.error("Spotify connection dropped for genre '%s'", genre)
            st.error("Lost connection to Spotify. Check your internet and try again.")
            if st.button("Retry"):
                st.rerun()
        except Exception as e:
            log.error("Unexpected error during Spotify search: %s", e)
            st.error("Something went wrong while searching Spotify. Try starting over.")
            if st.button("Start Over"):
                for key in list(st.session_state.keys()):
                    del st.session_state[key]
                st.rerun()

# Active chat
else:
    if user_input := st.chat_input("Tell me what you're in the mood for..."):
        log.info("User input: %s", user_input)
        st.session_state.messages.append({"role": "user", "content": user_input})

        with st.chat_message("user"):
            st.write(user_input)

        try:
            with st.chat_message("assistant"):
                response_text = st.write_stream(stream_response(st.session_state.messages))

            prefs = extract_prefs(response_text)
            if prefs:
                st.session_state.prefs = prefs
                display = re.sub(r"```json.*?```", "", response_text, flags=re.DOTALL).strip()
                if display:
                    st.session_state.messages.append({"role": "assistant", "content": display})
                st.session_state.messages.append(
                    {"role": "assistant", "content": "Got your taste! Searching Spotify now..."}
                )
            else:
                st.session_state.messages.append({"role": "assistant", "content": response_text})
        except Exception as e:
            log.error("Groq streaming error: %s", e)
            st.error("Lost connection to the AI. Please refresh the page and try again.")

        st.rerun()
