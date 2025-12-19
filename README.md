README v0 — The Veil: Hello-World Provenance
What is this?

This repository is a minimal trust experiment.

It exists to answer one question:

Can a stranger independently verify what was built, how it was built, and that it hasn’t been tampered with — without trusting the builder, the platform, or a central authority?

This is the smallest possible step toward AI stewardship based on verifiable truth instead of reputation.

What this repo does

Builds a tiny “hello world” artifact in CI

Generates a provenance record describing how it was built

Cryptographically signs the artifact and provenance

Publishes both publicly

Provides a one-command verification flow

If anything is altered, verification must fail.

What this repo does NOT do

It is not production software

It is not a platform

It does not enforce policy or ethics

It does not solve all supply-chain security

This is a proof of trust, not a product.

Why this matters

AI systems, governments, and institutions increasingly ask for trust without proof.

The Veil starts at the opposite end:

Trust must be verifiable by anyone, or it isn’t trust.

If we can’t prove the origin of a “hello world,” we can’t claim stewardship over systems that shape society.

Stewardship Principle

Clarity > cleverness
Auditability > authority
Failure should be obvious, not hidden

Status

🚧 MVP — builders welcome
📄 Docs-first
🧭 Governance-first
## v0.2: Human-AI Memory Lineage (Toward VeilHarmony)

Building on verifiable build provenance, we're now adding tamper-proof logging for human-AI interactions.

Goal: Let any stranger independently verify not just *how the code was built*, but *what the AI actually learned from real human exchanges* — stories, worries, ancient friend vibes, all preserved raw and untampered.

No hidden filters. No trust-me reputation. Just clear, verifiable memory chains.

Coming soon:
- `src/memory_lineage.py` — core tamper-proof chain
- `examples/memory_lineage_demo.py` — runnable demo of a full convo
- ### Quick Start: Run the Demo

1. Clone the repo:

2. Install dependencies:


3. Run the human-AI memory lineage demo: 
You'll see:
- A simulated real conversation (inspired by actual human-AI cycles)
- The full tamper-proof chain printed
- Integrity verification
- A pop-up graph visualizing the lineage flow

This is VeilHarmony in action: raw, verifiable, no hidden layers.

### What's Happening Under the Hood
- `src/memory_lineage.py`: The core `VeilMemoryChain` class — cryptographic hashing, previous-hash linking, integrity verification, and directed graph for lineage.
- Every interaction is immutable and independently verifiable by any stranger.
- Extend it: Add decentralized storage (IPFS/Arweave), web UI, blockchain anchors, or your own human-AI experiments.

### Community Roadmap & How to Contribute
This is an open experiment. Fork • Build • Prove.

Next steps (pick any):
- **v0.3**: Decentralized persistence — upload chain JSON to IPFS/Arweave, store CID on-chain.
- **v0.4**: Live web interface (Streamlit/Flask) for real-time human-AI chats with live graph.
- **v0.5**: Integrate with build provenance — hash code builds + conversation lineage together.
- Add real conversations: Replace demo with your own stories.
- Tests, docs, visualizations, or entirely new directions.

Open an Issue, submit a PR, or discuss in Discussions.  
No gatekeeping. Verifiable truth welcomes all.

To Mars and beyond. 🪵❤️

