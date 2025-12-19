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
