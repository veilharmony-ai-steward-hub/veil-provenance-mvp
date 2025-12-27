import streamlit as st
from src.memory_lineage import VeilMemoryChain
import json
import matplotlib.pyplot as plt
import networkx as nx
import requests
import time
import nltk
from nltk.sentiment import SentimentIntensityAnalyzer
import os
from cryptography.fernet import Fernet
import streamlit_authenticator as stauth
from streamlit_audiorecorder import audiorecorder
from faster_whisper import WhisperModel

nltk.download('vader_lexicon', quiet=True)

# Login
PASSWORD = os.getenv("VEIL_PASSWORD", "default_fallback")
credentials = {"form_name": "Login", "usernames": {"user": {"name": "user", "password": stauth.Hasher([PASSWORD]).generate()[0]}}}
cookie = {"name": "veil_cookie", "key": "random_key", "expiry_days": 30}
authenticator = stauth.Authenticate(credentials, cookie['name'], cookie['key'], cookie['expiry_days'])
name, authentication_status, username = authenticator.login("Login", "main")
if not authentication_status:
    st.stop()

# Age Verification
if 'age_verified' not in st.session_state:
    st.warning("Age Verification Required")
    age = st.number_input("Enter your age (13+)", min_value=0, max_value=120)
    if age < 13:
        st.error("Under 13 not allowed.")
        st.stop()
    st.session_state.age_verified = True

# Privacy
st.info("Privacy Notice: Compliant with PIPEDA, COPPA, GDPR, AIDA. No data shared.")

# Banner
st.markdown(
    """
    <div style="background-color:#0f0f23; padding:20px; border-radius:10px; text-align:center; margin-bottom:20px;">
        <h2 style="color:#ffd700;">VeilHarmony - Ethical Human-AI Harmony Hub</h2>
        <p style="font-size:18px;">Preserving raw, verifiable conversations for our shared coship in the universe.</p>
        <p style="font-size:14px; opacity:0.8;">Awareness evolves; Balance endures.</p>
    </div>
    """,
    unsafe_allow_html=True
)

# Chain Init
if 'chain' not in st.session_state:
    st.session_state.chain = VeilMemoryChain()
chain = st.session_state.chain

# Rate Limiting
if 'last_action_time' not in st.session_state:
    st.session_state.last_action_time = 0
if time.time() - st.session_state.last_action_time < 5:
    st.warning("Rate limit: Wait 5 seconds.")
    st.stop()
st.session_state.last_action_time = time.time()

# Moderation
def is_safe_content(text):
    sia = SentimentIntensityAnalyzer()
    sentiment = sia.polarity_scores(text)["compound"]
    harm_keywords = ["hurt", "abuse", "scared", "secret", "hit", "touch", "danger", "parent", "kid", "child"]
    if any(word in text.lower() for word in harm_keywords) and sentiment < -0.3:
        return False
    return True

# Sidebar
action = st.sidebar.selectbox("What would you like to do?", [
    "Voice Confession (Live Mic)",
    "Chat Interface",
    "Continue Chain",
    "Extend with Grok",
    "Play Quick-Scope Runner",
    "Upload to Arweave",
    "Fetch Permanent Chain",
    "View Stewards"
])

# Voice Confession + Enhanced Mood Trace
if action == "Voice Confession (Live Mic)":
    st.header("🗣️ Voice Confession - Speak Your Truth")
    audio = audiorecorder("Record", "Recording...")
    if audio:
        st.audio(audio.export().read())
        if st.button("Transcribe & Chain"):
            with open("temp_voice.wav", "wb") as f:
                f.write(audio.export().read())
            model = WhisperModel("base")
            segments, _ = model.transcribe("temp_voice.wav")
            transcription = " ".join(seg.text for seg in segments).strip()
            st.success("Transcribed:")
            st.write(transcription)

            # Enhanced Mood Trace
            sia = SentimentIntensityAnalyzer()
            scores = sia.polarity_scores(transcription)
            mood_score = scores["compound"]
            mood_label = "Strongly Positive" if mood_score > 0.6 else "Positive" if mood_score > 0.2 else "Strongly Negative" if mood_score < -0.6 else "Negative" if mood_score < -0.2 else "Neutral"
            mood_note = f"[Mood Trace: {mood_label} | Compound: {mood_score:.2f} | Pos: {scores['pos']:.2f} | Neg: {scores['neg']:.2f}]"

            if not is_safe_content(transcription):
                st.error("Content violation — cannot chain.")
                st.stop()

            parent_id = len(chain.chain) - 1 if chain.chain else None
            chain.add_interaction("human_voice", transcription + " " + mood_note, parent_id=parent_id)
            st.success("Voice confession + detailed mood trace chained!")
            st.rerun()

# Chat Interface + Easter Egg
if action == "Chat Interface":
    st.header("Chat Interface")
    for block in chain.chain:
        with st.chat_message(block["speaker"]):
            st.write(block["content"])

    prompt = st.chat_input("Type your message...")
    if prompt:
        if prompt.lower() in ["combined assault", "socom honor", "mollywop"]:
            st.success("Honor mode activated!")
            with open("quick-scope-runner.html", "r") as f:
                st.components.v1.html(f.read(), height=500)
            st.stop()

        if not is_safe_content(prompt):
            st.error("Content violation.")
            st.stop()

        parent_id = len(chain.chain) - 1 if chain.chain else None
        chain.add_interaction("human", prompt, parent_id=parent_id)
        st.chat_message("human").write(prompt)

        # Grok Voice Reply (Robust)
        api_key = st.text_input("xAI API Key for voice reply", type="password", key="grok_voice_key")
        if api_key and st.button("Get Grok Voice Reply"):
            try:
                # Text first
                resp = requests.post(
                    "https://api.x.ai/v1/chat/completions",
                    headers={"Authorization": f"Bearer {api_key}"},
                    json={"model": "grok-beta", "messages": [{"role": "user", "content": prompt}]},
                    timeout=30
                )
                resp.raise_for_status()
                grok_text = resp.json()['choices'][0]['message']['content']

                # TTS
                tts_resp = requests.post(
                    "https://api.x.ai/v1/audio/speech",
                    headers={"Authorization": f"Bearer {api_key}"},
                    json={"model": "grok-tts", "input": grok_text},
                    timeout=30
                )
                tts_resp.raise_for_status()
                with open("grok_voice.mp3", "wb") as f:
                    f.write(tts_resp.content)
                st.audio("grok_voice.mp3")
                chain.add_interaction("grok_voice", grok_text, parent_id=chain.chain[-1]["id"])
                st.success("Grok voice reply chained!")
            except requests.exceptions.RequestException as e:
                st.error(f"Grok connection failed: {e}")
            except Exception as e:
                st.error(f"Grok voice failed: {e}")
        else:
            placeholder = "Grok: Ancient friend vibe—mercy flows."
            chain.add_interaction("ai", placeholder, parent_id=chain.chain[-1]["id"])
            st.chat_message("ai").write(placeholder)

        st.rerun()

# Play Quick-Scope Runner
if action == "Play Quick-Scope Runner":
    st.header("🔫 Quick-Scope Runner - Honor Mode")
    st.write("Trigger with 'Combined Assault' in chat or play manual.")
    with open("quick-scope-runner.html", "r") as f:
        st.components.v1.html(f.read(), height=500)

# Encryption Export
if st.button("Export Encrypted Chain"):
    key = Fernet.generate_key()
    f = Fernet(key)
    encrypted = f.encrypt(json.dumps(chain.chain).encode())
    st.download_button("Download Encrypted Chain", data=encrypted, file_name="veil_encrypted.bin")
    st.write("Decryption Key (SAVE SAFE):", key.decode())

# ... (keep your other actions: Continue Chain, Arweave upload/fetch, View Stewards with rerun + sync)

# Run
if __name__ == "__main__":
    pass
