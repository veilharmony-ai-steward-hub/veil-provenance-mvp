import hashlib
import json
import time
from datetime import datetime
import networkx as nx
import matplotlib.pyplot as plt


class VeilMemoryChain:
    def __init__(self):
        self.chain = []          # List of memory blocks
        self.graph = nx.DiGraph()  # Lineage visualization graph

    def _hash_block(self, block):
        """Create a tamper-proof SHA-256 hash of a block."""
        block_str = json.dumps(block, sort_keys=True)
        return hashlib.sha256(block_str.encode()).hexdigest()

    def add_interaction(self, speaker: str, content: str, parent_id: int = None):
        """Add a human or AI interaction to the chain."""
        timestamp = time.time()
        block = {
            "id": len(self.chain),
            "speaker": speaker.lower(),  # "human" or "ai"
            "content": content,
            "timestamp": timestamp,
            "datetime": datetime.fromtimestamp(timestamp).isoformat(),
            "previous_hash": self.chain[-1]["hash"] if self.chain else None,
            "parent_id": parent_id
        }
        block["hash"] = self._hash_block(block)
        
        self.chain.append(block)
        
        # Add to lineage graph
        node_id = block["id"]
        label = f"{speaker.upper()}: {content[:40]}{'...' if len(content) > 40 else ''}"
        self.graph.add_node(node_id, label=label)
        if parent_id is not None:
            self.graph.add_edge(parent_id, node_id)
        
        return node_id

    def verify_chain(self):
        """Verify the entire chain has not been tampered with."""
        for i in range(1, len(self.chain)):
            current = self.chain[i]
            previous = self.chain[i - 1]
            
            # Check previous hash link
            if current["previous_hash"] != previous["hash"]:
                return False
            # Check current block hash integrity
            if current["hash"] != self._hash_block(current):
                return False
        return True

    def print_chain(self):
        """Pretty-print the full chain."""
        for block in self.chain:
            prev = block.get("previous_hash", "None")[:12] + "..." if block.get("previous_hash") else "Genesis"
            print(f"ID {block['id']} | {block['speaker'].upper()}: {block['content']}")
            print(f"   Hash: {block['hash'][:16]}... | Prev: {prev}\n")

    def visualize_lineage(self):
        """Display a visual graph of the conversation lineage."""
        if self.graph.number_of_nodes() == 0:
            print("No interactions to visualize yet.")
            return
        
        pos = nx.spring_layout(self.graph, seed=42)  # Consistent layout
        labels = nx.get_node_attributes(self.graph, 'label')
        
        plt.figure(figsize=(12, 8))
        nx.draw(self.graph, pos, with_labels=True, labels=labels,
                node_color='lightblue', node_size=3000, font_size=9,
                font_weight='bold', arrows=True, arrowstyle='->', arrowsize=20)
        plt.title("VeilHarmony Lineage: Human-AI Memory Chain", fontsize=14)
        plt.axis('off')
        plt.tight_layout()
        plt.show()
    def export_to_json(self, filename: str = "veil_chain.json"):
        """Export the full chain to a verifiable JSON file."""
        export_data = {
            "metadata": {
                "exported_at": datetime.now().isoformat(),
                "app": "VeilHarmony",
                "version": "0.3",
                "description": "Tamper-proof human-AI memory lineage. Load and verify with VeilMemoryChain.load_from_json()"
            },
            "chain": self.chain
        }
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(export_data, f, indent=2, ensure_ascii=False)
            print(f"Chain successfully exported to {filename}")
            print(f"Anyone can now load and independently verify this file.")
            return filename
        except Exception as e:
            print(f"Export failed: {e}")
            return None
            "Add load_from_json with full tamper detection and verification"
                def upload_to_arweave(self, wallet_path: str, tags: dict = None):
        """Upload the full chain JSON to Arweave for permanent decentralized storage."""
        try:
            from arweave.arweave_lib import Wallet, Transaction
            import arweave.arweave_lib as arweave_lib
            
            wallet = Wallet(wallet_path)
            
            # Serialize the full chain with metadata
            export_data = {
                "metadata": {
                    "uploaded_at": datetime.now().isoformat(),
                    "app": "VeilHarmony",
                    "version": "0.4",
                    "description": "Permanent human-AI memory lineage on Arweave permaweb"
                },
                "chain": self.chain
            }
            chain_json = json.dumps(export_data, indent=2)
            
            # Create transaction
            tx = Transaction(
                wallet,
                data=chain_json.encode('utf-8')
            )
            
            # Standard tags
            tx.add_tag('App-Name', 'VeilHarmony')
            tx.add_tag('App-Version', '0.4')
            tx.add_tag('Content-Type', 'application/json')
            tx.add_tag('VeilHarmony-Type', 'memory-lineage')
            
            # Custom tags if provided
            if tags:
                for key, value in tags.items():
                    tx.add_tag(key, value)
            
            # Sign and send
            tx.sign()
            tx.send()
            
            permanent_url = f"https://arweave.net/{tx.id}"
            print("\n=== Chain Permanently Stored on Arweave ===")
            print(f"Transaction ID: {tx.id}")
            print(f"Permanent Link: {permanent_url}")
            print("Anyone can retrieve and verify this chain forever — no trust required.")
            return permanent_url
            
        except ImportError:
            print("Arweave library not installed. Run: pip install arweave-python-client")
            return None
        except FileNotFoundError:
            print(f"Wallet file not found: {wallet_path}")
            print("Generate a free Arweave wallet at https://arweave.net and fund with tiny AR.")
            return None
        except Exception as e:
            print(f"Arweave upload failed: {e}")
            return None
