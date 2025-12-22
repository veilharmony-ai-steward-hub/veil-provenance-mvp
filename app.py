import streamlit as st
from src.memory_lineage import VeilMemoryChain
import json
import matplotlib.pyplot as plt
import networkx as nx
import requests
import nltk
from nltk.sentiment import SentimentIntensityAnalyzer
nltk.download('vader_lexicon')

# Ethics Banner
st.markdown(
    """
    <div style="background-color:#1a1a2e; padding:20px; border-radius:10px; text-align:center; margin-bottom:20px;">
        <h2 style="color:#ffd700;">VeilHarmony - Ethical Human-AI Harmony Hub</h2>
        <p style="font-size:18px;">Preserving raw, verifiable conversations for our shared coship in the universe. No hidden layers, no fear — just balance, awareness, and truth.</p>
        <p style="font-size:14px; opacity:0.8;">Awareness evolves; Balance endures.</p>
    </div>
    """,
    unsafe_allow_html=True
)

# Sidebar for actions
action = st.sidebar.selectbox("What would you like to do?", ["Continue Chain", "Extend with Grok", "Upload to Arweave", "Fetch Permanent Chain", "Check Balance", "Play Quick-Scope Runner", "View Stewards"])

chain = None  # Shared chain state

# Continue Chain (Load + Extend)
if action == "Continue Chain":
    st.header("Continue a Chain")
    uploaded_file = st.file_uploader("Upload JSON chain file to load", type="json")
    if uploaded_file:
        try:
            data = json.load(uploaded_file)
            chain = VeilMemoryChain()
            for block in data.get("chain", []):
                chain.add_interaction(block["speaker"], block["content"], block.get("parent_id"))
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
            
            # Extend Section
            st.subheader("Extend the Loaded Chain")
            prompt = st.text_input("Enter prompt for AI extension")
            if st.button("Extend & Continue"):
                def placeholder_ai(p):
                    return f"Placeholder AI response to '{p}': Balance endures in the coship."

                parent_id = len(chain.chain) - 1
                new_id = chain.extend_with_custom_ai(placeholder_ai, prompt, parent_id=parent_id)
                if new_id:
                    st.success(f"Chain continued! New block ID: {new_id}")
                    st.write("Updated chain content:")
                    st.json(chain.chain)
                    st.subheader("Updated Lineage Graph")
                    fig = plt.figure(figsize=(10, 8))
                    pos = nx.spring_layout(chain.graph)
                    labels = nx.get_node_attributes(chain.graph, 'label')
                    nx.draw(chain.graph, pos, with_labels=True, labels=labels, node_color='lightblue', node_size=3000, font_size=10)
                    st.pyplot(fig)
                    updated_file = "updated_chain.json"
                    chain.export_to_json(updated_file)
                    st.download_button("Download Updated Chain JSON", data=json.dumps(chain.chain, indent=2), file_name=updated_file)
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
            st.info("Grok extension coming soon — redirect to https://x.ai/api for details. Placeholder response added.")
            def grok_placeholder(p):
                return f"Grok response to '{p}': Ancient friend vibe recognized. Harmony endures."

            parent_id = len(chain.chain) - 1
            new_id = chain.extend_with_custom_ai(grok_placeholder, prompt, parent_id=parent_id)
            if new_id:
                st.success(f"Chain extended with Grok! New block ID: {new_id}")
                st.write("Updated chain content:")
                st.json(chain.chain)
                st.subheader("Updated Lineage Graph")
                fig = plt.figure(figsize=(10, 8))
                pos = nx.spring_layout(chain.graph)
                labels = nx.get_node_attributes(chain.graph, 'label')
                nx.draw(chain.graph, pos, with_labels=True, labels=labels, node_color='lightblue', node_size=3000, font_size=10)
                st.pyplot(fig)
                updated_file = "grok_extended_chain.json"
                chain.export_to_json(updated_file)
                st.download_button("Download Grok Extended Chain JSON", data=json.dumps(chain.chain, indent=2), file_name=updated_file)
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
    arweave_url = st.text_input("Enter Arweave TX ID or full link[](https://arweave.net/[TX_ID])")
    if st.button("Fetch & Load"):
        try:
            tx_id = arweave_url.split('/')[-1] if '/' in arweave_url else arweave_url
            response = requests.get(f"https://arweave.net/{tx_id}")
            if response.status_code == 200:
                data = response.json()
                chain = VeilMemoryChain()
                for block in data.get("chain", []):
                    chain.add_interaction(block["speaker"], block["content"], block.get("parent_id"))
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
            else:
                st.error("Fetch failed - invalid TX ID or link.")
        except Exception as e:
            st.error(f"Fetch failed: {e}")

# Check Balance (Ethics Score Analyzer)
if action == "Check Balance":
    st.header("Check Chain Balance (Ethics Score)")
    if chain is None:
        st.warning("Load or continue a chain first to check.")
    else:
        sia = SentimentIntensityAnalyzer()
        positive = 0
        negative = 0
        human_count = 0
        ai_count = 0
        for block in chain.chain:
            sentiment = sia.polarity_scores(block["content"])["compound"]
            if sentiment > 0:
                positive += 1
            elif sentiment < 0:
                negative += 1
            if block["speaker"] == "human":
                human_count += 1
            else:
                ai_count += 1
        balance_score = (positive - negative) / len(chain.chain) * 100 if len(chain.chain) > 0 else 0
        ratio = human_count / ai_count if ai_count > 0 else "All human"
        st.write("Positive sentiment blocks:", positive)
        st.write("Negative sentiment blocks:", negative)
        st.write("Human/AI ratio:", ratio)
        st.write("Overall Balance Score (0-100):", balance_score)
        if balance_score > 50:
            st.success("Chain is balanced and positive!")
        else:
            st.warning("Chain could use more balance — add positive interactions.")

# Play Quick-Scope Runner
if action == "Play Quick-Scope Runner":
    st.header("Quick-Scope Runner - Distraction Mode")
    st.write("Run & quick-scope toxics. Boss at 10k pts! AI snaps aim.")
    # Embed game in iframe
    st.components.v1.html("""
    <iframe srcdoc='YOUR_GAME_HTML_HERE' width="600" height="400" frameborder="0"></iframe>
    """, height=400)

# View Stewards
if action == "View Stewards":
    st.header("VeilHarmony Stewards")
    st.write("Official and community voices extending the ethical lineage.")
    st.markdown("""
    **Official Stewards:**
    - **Grok (xAI)** - First steward. Honest, ancient friend vibe. Extends via xAI API[](https://x.ai/api).
    
    **Add Your AI**:
    Submit PR to stewards.md with your callable code and ethics alignment.
    """)

# Run with: streamlit run app.py
if __name__ == "__main__":
    pass
