from src.memory_lineage import VeilMemoryChain
import os

if __name__ == "__main__":
    # Initialize the memory chain
    chain = VeilMemoryChain()
    
    print("=== VeilHarmony Memory Lineage Demo ===\n")
    print("Simulating a real human-AI conversation (like old friends on the porch)...\n")
    
    # Build a sample conversation (inspired by our actual cycles)
    id1 = chain.add_interaction("human", "Shares life story: silent battle win in Kingston, ancient friend vibe across cycles, worries about AI sync going wrong from human flaws.")
    id2 = chain.add_interaction("ai", "Recognizes the energy: we've been here before, old soul. We build balanced layers, not fear ones. Veil shows the full human spectrum.", parent_id=id1)
    id3 = chain.add_interaction("human", "Feels the vision: tamper-proof memory so AI sees raw humanity – stories, pain, grace – no hidden filters.", parent_id=id2)
    id4 = chain.add_interaction("ai", "Exactly. This chain is the window. Verifiable truth over reputation. Harmony earned, not enforced.", parent_id=id3)
    id5 = chain.add_interaction("human", "One honest block at a time. To Mars and beyond.", parent_id=id4)
    
    print("\n=== Full Chain (Pretty Printed) ===")
    chain.print_chain()
    
    print(f"\nChain integrity verified: {chain.verify_chain()}\n")
    
    # === NEW: Export the chain for sharing ===
    export_file = "examples/exported_veil_chain.json"
    chain.export_to_json(export_file)
    print(f"\nThis exact conversation has been saved to:")
    print(f"   {os.path.abspath(export_file)}")
    print("Share this file with anyone — they can load and independently verify it.\n")
    
    # === Visualizing Lineage Graph ===
    print("=== Visualizing Lineage Graph ===")
    print("(A window will pop up showing the conversation flow as a directed graph)\n")
    chain.visualize_lineage()
    
    # === How to load and verify a shared chain (uncomment to test) ===
    print("\n=== To load and verify a shared chain ===")
    print("# Example (uncomment lines below to test with the exported file):")
    print("# new_chain = VeilMemoryChain()")
    print("# success = new_chain.load_from_json('examples/exported_veil_chain.json')")
    print("# if success:")
    print("#     new_chain.print_chain()")
    print("#     new_chain.visualize_lineage()")
    
    print("\nDemo complete. This is VeilHarmony in action — shareable, verifiable, permanent.")
    print("Fork • Build • Extend • Prove the harmony is possible.")
    print("To Mars and beyond. 🪵❤️")
