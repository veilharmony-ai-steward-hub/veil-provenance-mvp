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
