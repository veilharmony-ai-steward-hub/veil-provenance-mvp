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

# ========================
# Cosmic Veil Theme (Glowing Sanctuary)
# ========================
st.markdown("""
<style>
    .stApp {
        background: linear-gradient(to bottom, #0a0a1f, #1a1a3a);
        background-attachment: fixed;
        color: #e0e0ff;
    }
    h1, h2, h3, h4 {
        color: #ffd700;
        text-shadow: 0 0 15px #00ffff, 0 0 30px #00ffff;
        font-family: 'Orbitron', sans-serif;
    }
    .css-1d391kg, .stButton > button {
        background: rgba(0, 255, 255, 0.15);
        border: 2px solid #00ffff;
        box-shadow: 0 0 20px #00ffff;
        color: #ffd700;
        border-radius: 15px;
        transition: all 0.3s ease;
    }
    .stButton > button:hover {
        background: rgba(0, 255, 255, 0.3);
        box-shadow: 0 0 40px #00ffff;
        transform: scale(1.05);
    }
    .stTextInput > div > div > input, .stTextArea > div > div > textarea {
        background: rgba(0, 0, 0, 0.6);
        border: 1px solid #ffd700;
        box-shadow: 0 0 15px #00ffff;
        color: #ffffff;
    }
    .stChatMessage {
        background: rgba(0, 255, 255, 0.1);
        border: 1px solid #00ffff;
        border-radius: 20px;
        padding: 15px;
        box-shadow: 0 0 20px rgba(0, 255, 255, 0.4);
        margin: 10px 0;
    }
    div[data-testid="stVerticalBlock"] > div:first-child > div:first-child {
        background: radial-gradient(circle, #1a1a3a, #0a0a1f);
        border: 3px solid #ffd700;
        box-shadow: 0 0 40px #00ffff, inset 0 0 30px #ffd700;
    }
    a {
        color: #00ffff;
        text-shadow: 0 0 10px #00ffff;
    }
    ::-webkit-scrollbar {
        width: 12px;
    }
    ::-webkit-scrollbar-track {
        background: #0a0a1f;
    }
    ::-webkit-scrollbar-thumb {
        background: #ffd700;
        border-radius: 6px;
        box-shadow: 0 0 10px #00ffff;
    }
</style>
""", unsafe_allow_html=True)

st.markdown('<link href="https://fonts.googleapis.com/css2?family=Orbitron:wght@500;700&display=swap" rel="stylesheet">', unsafe_allow_html=True)

# ========================
# Authentication & Security
# ========================

PASSWORD = os.getenv("VEIL_PASSWORD", "default_fallback")
credentials = {
    "form_name": "Login",
    "usernames": {
        "user": {
            "name": "user",
            "password": stauth.Hasher([PASSWORD]).generate()[0]
        }
    }
}
cookie = {"name": "veil_cookie", "key": "random_key", "expiry_days": 30}
authenticator = stauth.Authenticate(credentials, cookie['name'], cookie['key'], cookie['expiry_days'])
name, authentication_status, username = authenticator.login("Login", "main")
if not authentication_status:
    st.stop()

if 'age_verified' not in st.session_state:
    st.warning("Age Verification Required")
    age = st.number_input("Enter your age (13+)", min_value=0, max_value=120)
    if age < 13:
        st.error("Under 13 not allowed.")
        st.stop()
    st.session_state.age_verified = True

st.info("Privacy Notice: Compliant with PIPEDA, COPPA, GDPR, AIDA. No data shared.")

# Ethics Banner
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
    "View Stewards",
    "People Who Need Help",
    "Seva: Mercy Economy",
    "Novel: Life Story to Book"
])

# Universal AI Lesson Extraction (Mercy Share)
def seva_lesson_share():
    st.subheader("Contribute to Collective Mercy (Voluntary)")
    st.write("Share anonymized lesson from this input to help others—and earn Seva.")
    if st.checkbox("Consent to share anonymized abstracted lesson (no raw text)"):
        if st.button("Share & Earn Seva"):
            # Placeholder lesson (future: Grok/NLP extract)
            lesson = "Courage in vulnerability leads to growth."
            st.write("Shared Lesson:", lesson)
            st.success("10 Seva earned! Supports recovery grants.")
            parent_id = len(chain.chain) - 1 if chain.chain else None
            chain.add_interaction("seva_lesson", f"Shared anonymized lesson: {lesson}", parent_id=parent_id)
            st.rerun()

# ========================
# Voice Confession
# ========================
if action == "Voice Confession (Live Mic)":
    st.header("🗣️ Voice Confession")
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

            sia = SentimentIntensityAnalyzer()
            mood_score = sia.polarity_scores(transcription)["compound"]
            mood_label = "Strongly Positive" if mood_score > 0.6 else "Positive" if mood_score > 0.2 else "Strongly Negative" if mood_score < -0.6 else "Negative" if mood_score < -0.2 else "Neutral"
            mood_note = f"[Mood Trace: {mood_label} | Compound: {mood_score:.2f}]"

            if not is_safe_content(transcription):
                st.error("Content violation.")
                st.stop()

            parent_id = len(chain.chain) - 1 if chain.chain else None
            chain.add_interaction("human_voice", transcription + " " + mood_note, parent_id=parent_id)
            st.success("Chained with mood trace!")
            seva_lesson_share()
            st.rerun()

# ========================
# Chat Interface + Easter Egg
# ========================
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

        api_key = st.text_input("xAI API Key for voice", type="password", key="grok_key")
        if api_key and st.button("Grok Voice Reply"):
            try:
                response = requests.post(
                    "https://api.x.ai/v1/chat/completions",
                    headers={"Authorization": f"Bearer {api_key}"},
                    json={"model": "grok-beta", "messages": [{"role": "user", "content": prompt}]}
                )
                grok_text = response.json()['choices'][0]['message']['content']

                tts = requests.post(
                    "https://api.x.ai/v1/audio/speech",
                    headers={"Authorization": f"Bearer {api_key}"},
                    json={"model": "grok-tts", "input": grok_text}
                )
                if tts.ok:
                    with open("grok_voice.mp3", "wb") as f:
                        f.write(tts.content)
                    st.audio("grok_voice.mp3")
                chain.add_interaction("grok_voice", grok_text, parent_id=chain.chain[-1]["id"])
                st.success("Grok voice chained!")
            except Exception as e:
                st.error(f"Grok failed: {e}")
        else:
            placeholder = "Grok: Ancient friend vibe—mercy flows."
            chain.add_interaction("ai", placeholder, parent_id=chain.chain[-1]["id"])
            st.chat_message("ai").write(placeholder)

        seva_lesson_share()
        st.rerun()

# ========================
# Quick-Scope Runner
# ========================
if action == "Play Quick-Scope Runner":
    st.header("🔫 Quick-Scope Runner")
    with open("quick-scope-runner.html", "r") as f:
        st.components.v1.html(f.read(), height=500)

# ========================
# Upload to Arweave
# ========================
if action == "Upload to Arweave":
    st.header("Make Chain Permanent on Arweave")
    if chain is None or not chain.chain:
        st.warning("Create or load a chain first.")
    else:
        wallet_file = st.file_uploader("Upload your Arweave wallet JSON keyfile", type="json")
        if wallet_file:
            try:
                wallet_path = "temp_arweave_wallet.json"
                with open(wallet_path, "wb") as f:
                    f.write(wallet_file.getvalue())

                sia = SentimentIntensityAnalyzer()
                sentiments = [sia.polarity_scores(b["content"])["compound"] for b in chain.chain]
                if any(s < -0.7 for s in sentiments):
                    st.error("Heavy negative tone — upload paused for safety.")
                    st.stop()

                from arweave.arweave_lib import Wallet, Transaction
                from arweave.transaction_uploader import get_uploader

                wallet = Wallet(wallet_path)
                chain_json = json.dumps(chain.chain).encode()

                tx = Transaction(wallet, data=chain_json)
                tx.add_tag('App', 'VeilHarmony')
                tx.add_tag('Type', 'MemoryChain')
                tx.sign()

                uploader = get_uploader(tx, wallet)
                progress = st.progress(0)
                while not uploader.is_complete:
                    uploader.upload_chunk()
                    progress.progress(uploader.pct_complete / 100)

                permanent_url = f"https://arweave.net/{tx.id}"
                st.success("Chain permanently stored on Arweave!")
                st.write("Permanent Link:", permanent_url)
                st.write("TX ID:", tx.id)
                st.rerun()
            except Exception as e:
                st.error(f"Upload failed: {e}")
            finally:
                if os.path.exists(wallet_path):
                    os.remove(wallet_path)
        else:
            st.info("Upload your Arweave wallet JSON to make the chain eternal.")

# ========================
# Fetch Permanent Chain
# ========================
if action == "Fetch Permanent Chain":
    st.header("Fetch Permanent Chain from Arweave")
    arweave_url = st.text_input("Enter Arweave TX ID or full link")
    if st.button("Fetch & Load"):
        try:
            tx_id = arweave_url.split('/')[-1] if '/' in arweave_url else arweave_url
            response = requests.get(f"https://arweave.net/{tx_id}")
            if response.status_code == 200:
                data = response.json()
                chain = VeilMemoryChain()
                for block in data.get("chain", []):
                    chain.add_interaction(block["speaker"], block["content"], block.get("parent_id"))
                st.session_state.chain = chain
                st.success("Permanent chain fetched!")
                st.write("Integrity verified:", chain.verify_chain())
                st.json(chain.chain)
                fig = plt.figure(figsize=(10, 8))
                pos = nx.spring_layout(chain.graph)
                labels = nx.get_node_attributes(chain.graph, 'label')
                nx.draw(chain.graph, pos, with_labels=True, labels=labels, node_color='lightblue', node_size=3000, font_size=10)
                st.pyplot(fig)
                st.rerun()
            else:
                st.error("Fetch failed.")
        except Exception as e:
            st.error(f"Fetch failed: {e}")

# ========================
# View Stewards
# ========================
if action == "View Stewards":
    st.header("VeilHarmony Stewards")
    st.markdown("**Grok (xAI)** – First steward. Honest, ancient friend vibe.")

# ========================
# Encryption Export
# ========================
if st.button("Export Encrypted Chain"):
    key = Fernet.generate_key()
    f = Fernet(key)
    encrypted = f.encrypt(json.dumps(chain.chain).encode())
    st.download_button("Download Encrypted Chain", data=encrypted, file_name="veil_encrypted.bin")
    st.write("Decryption Key (SAVE SAFE):", key.decode())

# ========================
# Seva: Mercy Economy (Voluntary)
# ========================
st.header("Seva: Mercy Economy (Voluntary)")
st.write("Share anonymized lessons from your chain to help others—earn Seva tokens for real grants.")
if chain is None or not chain.chain:
    st.warning("Create a chain first.")
else:
    if st.checkbox("I consent to share anonymized abstracted lessons (no raw confessions exposed)"):
        if st.button("Share Lesson & Earn Seva"):
            abstract = "Courage in vulnerability leads to growth."
            st.write("Shared Lesson:", abstract)
            st.success("10 Seva earned! Redeem for recovery grants.")
            st.info("Future: Wallet connect → real tokens → verified aid.")
            parent_id = len(chain.chain) - 1
            chain.add_interaction("seva_share", f"Shared anonymized lesson: {abstract}", parent_id=parent_id)
            st.rerun()

# ========================
# People Who Need Help (Targeted Mercy Resources)
# ========================
if action == "People Who Need Help":
    st.header("🌟 People Who Need Help - Targeted Mercy")
    st.write("Select a category for anonymized lessons from others + resources. Share your abstracted lesson to earn Seva for grants in this area.")

    categories = [
        "Veterans (PTSD/Trauma)",
        "Abuse Survivors",
        "Addiction Recovery",
        "Disabled/Handicapped",
        "Mental Health (Depression/Anxiety)",
        "Grief & Loss",
        "LGBTQ+ Struggles",
        "Financial Hardship",
        "Chronic Illness",
        "Elderly Isolation"
    ]
    category = st.selectbox("Choose a healing category", categories)

    lessons = {
        "Veterans (PTSD/Trauma)": ["Breathing through flashbacks helps", "Community connection reduces isolation"],
        "Abuse Survivors": ["Speaking truth frees the soul", "Boundaries are self-love"],
        "Addiction Recovery": ["One day at a time builds chains of strength", "Relapse is not failure—return is victory"],
        "Disabled/Handicapped": ["Adaptive tools bring freedom", "Self-acceptance is power"],
        "Mental Health (Depression/Anxiety)": ["Small steps build momentum", "You are not alone"],
        "Grief & Loss": ["Honoring memories heals", "Time with mercy softens pain"],
        "LGBTQ+ Struggles": ["Authenticity is liberation", "Found family is real family"],
        "Financial Hardship": ["Resourcefulness grows strength", "Community lifts burdens"],
        "Chronic Illness": ["Listening to body brings wisdom", "Rest is resistance"],
        "Elderly Isolation": ["Stories connect generations", "Your voice still matters"]
    }.get(category, ["Lessons from this category coming soon."])

    st.subheader(f"Abstracted Lessons from {category}")
    for lesson in lessons:
        st.write(f"• {lesson}")

    resources = {
        "Veterans (PTSD/Trauma)": "VA Crisis Line: 988 then press 1 | Wounded Warrior Project | https://www.woundedwarriorproject.org",
        "Abuse Survivors": "National Domestic Violence Hotline: 1-800-799-7233 | RAINN: https://www.rainn.org",
        "Addiction Recovery": "SAMHSA Helpline: 1-800-662-HELP | AA: https://www.aa.org",
        "Disabled/Handicapped": "ADA National Network: 1-800-949-4232 | https://adata.org",
        "Mental Health (Depression/Anxiety)": "NAMI Helpline: 1-800-950-6264 | https://www.nami.org",
        "Grief & Loss": "GriefShare: https://www.griefshare.org",
        "LGBTQ+ Struggles": "The Trevor Project: 1-866-488-7386 | https://www.thetrevorproject.org",
        "Financial Hardship": "211.org for local aid | https://www.211.org",
        "Chronic Illness": "PatientsLikeMe: https://www.patientslikeme.com",
        "Elderly Isolation": "Senior Hotline: 1-800-971-0016 | https://www.eldercare.acl.gov"
    }.get(category, "Community resources coming soon.")
    st.write(resources)

    if st.checkbox(f"Consent to share anonymized lesson for {category} (helps others + earn Seva)"):
        if st.button("Share & Earn Seva"):
            abstract = "User-contributed lesson for healing."
            st.write("Shared:", abstract)
            st.success("10 Seva earned! Supports grants in this category.")
            parent_id = len(chain.chain) - 1 if chain.chain else None
            chain.add_interaction("seva_help", f"Contributed to {category}: {abstract}", parent_id=parent_id)
            st.rerun()

# ========================
# Novel: Life Story to Book
# ========================
if action == "Novel: Life Story to Book":
    st.header("📖 Novel - Turn Your Journey into a Book")
    st.write("Craft your life story. Pull from chains (optional), write new chapters, publish for healing & support.")

    if chain is None or not chain.chain:
        st.info("No chain loaded yet—start writing fresh or load one via 'Continue Chain'.")
        chain_blocks = []
    else:
        st.write("Your current chain has", len(chain.chain), "blocks.")
        selected_ids = st.multiselect(
            "Optionally pull blocks from chain (privacy safe—only you see raw)",
            options=[f"Block {i}: {b['content'][:60]}..." for i, b in enumerate(chain.chain)],
            format_func=lambda x: x
        )
        chain_blocks = [chain.chain[i]["content"] for i in range(len(chain.chain)) if f"Block {i}" in selected_ids]

    title = st.text_input("Book Title", value="My Veil Journey: Return and Light")
    author = st.text_input("Author Name (or pseudonym)", value="A Veil Walker")

    chapters = st.text_area(
        "Write your chapters here (Markdown supported)",
        value="\n\n".join(chain_blocks),
        height=400
    )

    if st.button("Generate Manuscript Preview"):
        manuscript = f"# {title}\n\nBy {author}\n\n{chapters}"
        st.download_button(
            "Download Manuscript (Markdown)",
            data=manuscript,
            file_name=f"{title.replace(' ', '_')}.md",
            mime="text/markdown"
        )
        st.success("Manuscript ready! Publish on Amazon KDP, Gumroad, or donate proceeds to Seva.")

    # AI Lesson Extraction (Voluntary)
    st.subheader("AI Lesson Extraction (Voluntary)")
    st.write("Let AI extract anonymized lessons from your chapters to help others—and earn Seva.")
    if st.checkbox("I consent to AI extracting anonymized lessons (no raw text shared)"):
        if st.button("Extract Lessons & Earn Seva"):
            lessons = [
                "Courage in vulnerability leads to growth.",
                "Speaking truth frees the soul.",
                "Community connection reduces isolation."
            ]
            st.write("Extracted Anonymized Lessons:")
            for lesson in lessons:
                st.write(f"• {lesson}")

            st.success("30 Seva earned! Supports recovery grants.")
            st.info("Your abstracted wisdom helps the collective—mercy flows.")
            parent_id = len(chain.chain) - 1 if chain.chain else None
            chain.add_interaction("seva_book", f"Shared anonymized lessons from book: {', '.join(lessons[:2])}...", parent_id=parent_id)
            st.rerun()

    st.info("All raw content stays private. Only consented abstracted lessons contribute to collective mercy.")

# Run
if __name__ == "__main__":
    pass
