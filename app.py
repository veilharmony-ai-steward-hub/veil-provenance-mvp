import streamlit as st
from src.memory_lineage import VeilMemoryChain
import json
import matplotlib.pyplot as plt
import networkx as nx

st.title("VeilHarmony - Ethical Human-AI Harmony Hub")
st.write("Load, continue, extend, verify, and preserve chains forever. Ethical conversations for our coship.")

# Sidebar for actions
action = st.sidebar.selectbox("What would you like to do?", ["Continue Chain", "Upload to Arweave"])

# Continue Chain (Load + Extend)
if action == "Continue Chain":
    st.header("Continue a Chain")
    uploaded_file = st.file_uploader("Upload JSON chain file to load", type="json")
    if uploaded_file:
        try:
            data = json.load(uploaded_file)
            chain = VeilMemoryChain()
            # Rebuild chain
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
                # Placeholder AI callable (replace with real Grok or user AI later)
                def placeholder_ai(p):
                    return f"Placeholder AI response to '{p}': Balance endures in the coship."

                # Extend from last block (or user-selected parent)
                parent_id = len(chain.chain) - 1  # Last block as parent
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
                    # Export updated chain
                    updated_file = "updated_chain.json"
                    chain.export_to_json(updated_file)
                    st.download_button("Download Updated Chain JSON", data=json.dumps(chain.chain, indent=2), file_name=updated_file)
                else:
                    st.error("Extension failed.")
        except Exception as e:
            st.error(f"Load failed: {e}")

# Upload to Arweave (placeholder)
if action == "Upload to Arweave":
    st.header("Make Chain Permanent")
    st.write("Wallet upload coming in next update.")

# Run with: streamlit run app.py
if __name__ == "__main__":
    pass
