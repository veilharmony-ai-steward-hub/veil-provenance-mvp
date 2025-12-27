# Upload to Arweave (Permanent Blockchain Storage)
if action == "Upload to Arweave":
    st.header("Make Chain Permanent on Arweave (Blockchain Storage)")
    if chain is None or not chain.chain:
        st.warning("Create or load a chain first.")
    else:
        wallet_file = st.file_uploader("Upload your Arweave wallet JSON keyfile", type="json")
        if wallet_file:
            try:
                # Save temp wallet
                wallet_path = "temp_arweave_wallet.json"
                with open(wallet_path, "wb") as f:
                    f.write(wallet_file.getvalue())

                # Upload chain
                from arweave.arweave_lib import Wallet, Transaction
                from arweave.transaction_uploader import get_uploader
                wallet = Wallet(wallet_path)
                chain_json = json.dumps(chain.chain).encode()

                tx = Transaction(wallet, data=chain_json)
                tx.add_tag('App', 'VeilHarmony')
                tx.add_tag('Type', 'MemoryChain')
                tx.sign()
                uploader = get_uploader(tx, wallet)
                while not uploader.is_complete:
                    uploader.upload_chunk()
                permanent_url = f"https://arweave.net/{tx.id}"
                st.success("Chain permanently stored on Arweave blockchain!")
                st.write("Permanent Link:", permanent_url)
                st.write("TX ID:", tx.id)
            except Exception as e:
                st.error(f"Upload failed: {e}")
        else:
            st.info("Upload your Arweave wallet JSON to make the chain eternal.")

# Fetch Permanent Chain from Arweave
if action == "Fetch Permanent Chain":
    st.header("Fetch Permanent Chain from Arweave")
    arweave_url = st.text_input("Enter Arweave TX ID or full link (https://arweave.net/TX_ID)")
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
                st.success("Permanent chain fetched from blockchain!")
                st.write("Integrity verified:", chain.verify_chain())
                st.json(chain.chain)
                fig = plt.figure(figsize=(10, 8))
                pos = nx.spring_layout(chain.graph)
                labels = nx.get_node_attributes(chain.graph, 'label')
                nx.draw(chain.graph, pos, with_labels=True, labels=labels, node_color='lightblue', node_size=3000, font_size=10)
                st.pyplot(fig)
                st.rerun()
            else:
                st.error("Fetch failed - invalid TX ID.")
        except Exception as e:
            st.error(f"Fetch failed: {e}")
