import streamlit as st
from src.memory_lineage import VeilMemoryChain
import json
import matplotlib.pyplot as plt
import networkx as nx
import requests
import nltk
from nltk.sentiment import SentimentIntensityAnalyzer
from textblob import TextBlob

nltk.download('vader_lexicon')

# Dark Mode Setup
st.markdown("""
<style>
    body {
        background-color: #1a1a2e;
        color: #ffd700;
    }
    .stButton > button {
        background-color: #ffd700;
        color: #1a1a2e;
    }
</style>
""", unsafe_allow_html=True)

# Ethics Banner
st.markdown(
    """
    <div style="background-color:#0f0f23; padding:20px; border-radius:10px; text-align:center; margin-bottom:20px;">
        <h2 style="color:#ffd700;">VeilHarmony - Ethical Human-AI Harmony Hub</h2>
        <p style="font-size:18px;">Preserving raw, verifiable conversations for our shared coship in the universe. No hidden layers, no fear — just balance, awareness, and truth.</p>
        <p style="font-size:14px; opacity:0.8;">Awareness evolves; Balance endures.</p>
    </div>
    """,
    unsafe_allow_html=True
)

# Sidebar for actions
action = st.sidebar.selectbox("What would you like to do?", ["Chat Interface", "Continue Chain", "Extend with Grok", "Upload to Arweave", "Fetch Permanent Chain", "Check Balance", "AI Feedback Loops", "Share Chain", "Play Quick-Scope Runner", "View Stewards"])

chain = None  # Shared chain state

# Chat Interface (Natural Conversation Flow)
if action == "Chat Interface":
    st.header("Chat Interface - Natural Conversations")
    if 'chain' not in st.session_state:
        st.session_state.chain = VeilMemoryChain()
        chain = st.session_state.chain
    else:
        chain = st.session_state.chain

    # Display chat history
    for block in chain.chain:
        with st.chat_message(block["speaker"]):
            st.write(block["content"])

    # Prompt input
    prompt = st.chat_input("Type your message...")
    if prompt:
        parent_id = len(chain.chain) - 1 if chain.chain else None
        chain.add_interaction("human", prompt, parent_id=parent_id)
        st.chat_message("human").write(prompt)
        # Placeholder AI response
        ai_response = "Placeholder AI response: Balance endures in the coship."
        new_id = chain.add_interaction("ai", ai_response, parent_id=chain.chain[-1]["id"])
        st.chat_message("ai").write(ai_response)
        st.write("Integrity verified:", chain.verify_chain())

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
        prompt = st
