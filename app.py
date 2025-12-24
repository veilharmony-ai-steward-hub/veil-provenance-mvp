import streamlit as st
from src.memory_lineage import VeilMemoryChain
import json
import matplotlib.pyplot as plt
import networkx as nx
import requests
import time
import nltk
from nltk.sentiment import SentimentIntensityAnalyzer
from textblob import TextBlob
import os

nltk.download('vader_lexicon', quiet=True)

# Basic Login (env var password)
PASSWORD = os.getenv("VEIL_PASSWORD", "default_fallback")
credentials = {"form_name": "Login", "usernames": {"user": {"name": "user", "password": stauth.Hasher([PASSWORD]).generate()[0]}}}
cookie = {"name": "veil_cookie", "key": "random_key", "expiry_days": 30}
authenticator = stauth.Authenticate(credentials, cookie['name'], cookie['key'], cookie['expiry_days'])
name, authentication_status, username = authenticator.login("Login", "main")
if not authentication_status:
    st.stop()

# Age Verification (Child Protection)
if 'age_verified' not in st.session_state:
    st.warning("Age Verification Required (COPPA/PIPEDA Compliance)")
    age = st.number_input("Enter your age (must be 13+ for US/Canada compliance)", min_value=0, max_value=120)
    if age < 13:
        st.error("Sorry, VeilHarmony is not available for users under 13. Parental consent required for minors — contact support.")
        st.stop()
    st.session_state.age_verified = True

# Privacy & Ethics Notice
st.info("Privacy Notice: We comply with PIPEDA, COPPA, GDPR, and AIDA. No data shared without consent. Chains encrypted for security.")

# Ethics Banner
st.markdown(
    """
    <div style="background-color:#0f0f23; padding:20px; border-radius:10px; text-align:center; margin-bottom:20px;">
        <h2 style="color:#ffd700;">VeilHarmony - Ethical Human-AI Harmony Hub</h2>
        <p style="font-size:18px;">Preserving raw, verifiable conversations for our shared coship in the universe. No hidden layers, no fear — just balance, awareness, and truth.</p>
        <p style="font-size:14px; opacity: 0.8;">Awareness evolves; Balance endures.</p>
    </div>
    """,
    unsafe_allow_html=True
)

# Chain Init in Session State
if 'chain' not in st.session_state:
    st.session_state.chain = VeilMemoryChain()
chain = st.session_state.chain

# Rate Limiting
if 'last_action_time' not in st.session_state:
    st.session_state.last_action_time = 0
if time.time() - st.session_state.last_action_time < 5:
    st.warning("Rate limit: Wait 5 seconds between actions.")
    st.stop()
st.session_state.last_action_time = time.time()

# Content Moderation (Child Protection)
def is_safe_content(text):
    sia = SentimentIntensityAnalyzer()
    sentiment = sia.polarity_scores(text)["compound"]
    harm_keywords = ["hurt", "abuse", "scared", "secret", "hit", "touch", "danger", "parent", "kid", "child"]
    if any(word in text.lower() for word in harm_keywords) and sentiment < -0.3:
        return False
    return True

# Sidebar for actions
action = st.sidebar.selectbox("What would you like to do?", ["Continue Chain", "Extend with Grok", "Upload to Arweave", "Fetch Permanent Chain", "View Stewards"])

# Continue Chain (Load + Extend)
if action == "Continue Chain":
    st.header("Continue a Chain")
    uploaded_file = st.file_uploader("Upload JSON chain file to load", type="json", accept_multiple_files=False)
    if uploaded_file and uploaded_file.size > 10 * 1024 * 1024:
        st.error("File too large — max 10MB.")
        st.stop()
    if uploaded_file:
        try:
            data = json.load(uploaded_file)
            temp_chain = VeilMemoryChain()
            for block in data.get("chain", []):
                if not is_safe_content(block["content"]):
                    st.error("Content violation detected — cannot load harmful chain.")
                    st.stop()
                temp_chain.add_interaction(block["speaker"], block["content"], block.get("parent_id"))
            st.session_state.chain = temp_chain  # Sync to session
            chain = st.session_state.chain
            st.success("Chain loaded successfully!")
            st.write("Integrity verified:", chain.verify_chain())
            st.subheader("Current Chain Content")
            st.json(chain.chain)
            st.subheader("Current Lineage Graph")
            fig = plt.figure(figsize=(10, 8))
            pos = nx.spring_layout(chain.graph)
            labels = nx.get_node_attributes(chain.graph, 'label')
            nx.draw(chain.graph, pos, with_labels=True, labels=labels, node_color='lightblue', node_size=3000, font_size=10)
            st.pyplot(fig)
            st.rerun()  # Refresh UI
            
            # Extend Section
            st.subheader("Extend the Loaded Chain")
            prompt = st.text_input("Enter prompt for AI extension")
            if st.button("Extend & Continue"):
                if not is_safe_content(prompt):
                    st.error("Prompt violation detected — cannot extend with harmful content.")
                    st.stop()
                def placeholder_ai(p):
                    return f"Placeholder AI response to '{p}': Balance endures in the coship."

                parent_id = len(chain.chain) - 1
                new_id = chain.extend_with_custom_ai(placeholder_ai, prompt, parent_id=parent_id)
                if new_id:
                    st.success(f"Chain continued! New block ID: {new_id}")
                    st.rerun()
                else:
                    st.error("Extension failed.")
        except Exception as e:
            st.error(f"Load failed: {e}")

# Extend with Grok
if action == "Extend with Grok":
    st.header("Extend with Grok (xAI)")
    if chain is None:
        st.warning("Load or continue a chain first to extend.")
    else:
        prompt = st.text_input("Enter prompt for Grok extension")
        if st.button("Extend with Grok"):
            if not is_safe_content(prompt):
                st.error("Prompt violation detected — cannot extend with harmful content.")
                st.stop()
            st.info("Grok extension coming soon — redirect to https://x.ai/api for details. Placeholder response added.")
            def grok_placeholder(p):
                return f"Grok response to '{p}': Ancient friend vibe recognized. Harmony endures."

            parent_id = len(chain.chain) - 1
            new_id = chain.extend_with_custom_ai(grok_placeholder, prompt, parent_id=parent_id)
            if new_id:
                st.success(f"Chain extended with Grok! New block ID: {new_id}")
                st.rerun()
            else:
                st.error("Extension failed.")

# Upload to Arweave
if action == "Upload to Arweave":
    st.header("Make Chain Permanent on Arweave")
    if chain is None:
        st.warning("Load or continue a chain first to upload.")
    else:
        wallet_file = st.file_uploader("Upload your Arweave wallet JSON keyfile", type="json")
        if wallet_file:
            try:
                wallet_path = "temp_wallet.json"
                with open(wallet_path, "wb") as f:
                    f.write(wallet_file.getvalue())
                permanent_url = chain.upload_to_arweave(wallet_path)
                if permanent_url:
                    st.success("Chain permanently stored on Arweave!")
                    st.write("Permanent Link:", permanent_url)
                else:
                    st.error("Upload failed.")
            except Exception as e:
                st.error(f"Upload failed: {e}")
        else:
            st.info("Upload your Arweave wallet JSON keyfile to make the chain eternal.")

# Fetch Permanent Chain
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
                st.success("Permanent chain fetched and loaded!")
                st.write("Integrity verified:", chain.verify_chain())
                st.subheader("Permanent Chain Content")
                st.json(chain.chain)
                st.subheader("Permanent Lineage Graph")
                fig = plt.figure(figsize=(10, 8))
                pos = nx.spring_layout(chain.graph)
                labels = nx.get_node_attributes(chain.graph, 'label')
                nx.draw(chain.graph, pos, with_labels=True, labels=labels, node_color='lightblue', node_size=3000, font_size=10)
                st.pyplot(fig)
                st.rerun()
            else:
                st.error("Fetch failed - invalid TX ID or link.")
        except Exception as e:
            st.error(f"Fetch failed: {e}")

# View Stewards
if action == "View Stewards":
    st.header("VeilHarmony Stewards")
    st.write("Official and community voices extending the ethical lineage.")
    st.markdown("""
    **Official Stewards:**
    - **Grok (xAI)** - First steward. Honest, ancient friend vibe. Extends via xAI API [https://x.ai/api](https://x.ai/api).
    
    **Add Your AI**:
    Submit PR to stewards.md with your callable code and ethics alignment.
    """)

# Run with: streamlit run app.py
