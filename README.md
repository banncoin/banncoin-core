🪙 Banncoin Core

Banks fail. Chains prevail.
A sovereign, miner-anchored blockchain protocol.

<div style="margin-top:10px;margin-bottom:20px;">

Status: Active
License: Banncoin Open Use License
Language: Python + HTML/CSS/JS
Eras: A (bootstrap) → B (economic, active)

</div>
📦 What This Repository Contains
Folder	Purpose
miner/	Official open-source Harmonic Miner
node/	Reference node implementation
site/	Public JSON feeds (status.json, recent.json, etc.)
scripts/	Exporters, utilities, non-sensitive helpers
docs/	Public documentation, manifests, explorer mirrors

This repository contains no secrets, no admin commands, no infrastructure, and no sensitive data.

⚡ Quickstart — Miner Developer Edition
git clone https://github.com/banncoin/banncoin-core.git
cd banncoin-core/miner
python3 bnc_miner.py \
  --api https://node.banncoin.org \
  --reward-to YOUR_WALLET \
  --log-dir ./miner_logs


✔ Works on Linux, macOS, WSL2
✔ CPU-friendly
✔ Era B compliant
✔ Auto-adapts to difficulty

Never mine to placeholders like YOUR_WALLET.
Use your own Banncoin address (bnc1…).

🔧 Public JSON Feeds (Open API)
Endpoint	Description
/docs/status.json	Network health & difficulty
/docs/recent.json	Recent block summaries
/docs/manifest.json	Chain metadata

All files under site/docs/ are safe, public-facing, and auto-updated.

🧱 Architecture Overview

See: ARCHITECTURE_OVERVIEW.md

Covers:

Era system

Block flow

Miner → Node → Chain relationship

Status + manifest format

Public metadata rules

🧭 Contribution Guidelines

See: CONTRIBUTING.md

No logs, keys, tokens, IPs

No binaries in repo

Keep PRs focused

Add tests where relevant

🔐 Security

See: SECURITY.md
Report vulnerabilities to contact@banncoin.org
.

🪶 Motto

“Value grows where no master can touch.”

Paste that into the README.md file inside the GitHub GUI and commit.

This is C1 = complete.

✅ C2 — Internal Docs Alignment

We update two internal docs to look fully professional and aligned:

1. ARCHITECTURE_OVERVIEW.md
2. CONTRIBUTING.md

These contain NO operational info, only high-level developer documentation.

1️⃣ ARCHITECTURE_OVERVIEW.md (Final, Safe Version)

Open GitHub GUI → banncoin-core → ARCHITECTURE_OVERVIEW.md → Edit
Paste this:

🧩 Banncoin Architecture Overview

Banncoin is a sovereign, miner-anchored blockchain protocol structured into two eras:

Era A — Bootstrap
Non-economic blocks used to initialize the chain.

Era B — Economic Era
Fully active mining, real rewards, difficulty retargeting.

This document describes the public architecture of the miner, node, public JSON outputs, and site metadata.

🔗 System Components
1. Miner

CPU-based Harmonic hashing loop

Fetches template → computes nonces → submits valid blocks

Stateless; all authoritative state lives on the node

Uses /status to get difficulty_bits, height, and target_seconds

2. Node

Receives block submissions

Validates difficulty, timestamp, reward, parent hash

Updates chain state

Publishes public JSON (status.json, recent.json, manifest.json)

3. Public Metadata

Directory: site/docs/

status.json → chain tip, difficulty

recent.json → recent blocks

manifest.json → chain metadata and structural info

All safe for public consumption.

🔄 Block Lifecycle

Miner requests block template

Miner computes nonces

Valid block → submit → node validates

Node commits new block

JSON feeds update

Explorers read public endpoints

🌐 Node Endpoint Rules

All public miners use:
https://node.banncoin.org

Responses are stable and versioned

No sensitive output is published

🧱 Eras
Era	Description	Rewards
A	Bootstrap	Non-spendable
B	Active chain	Spendable mining rewards
🎯 Design Principles

Simplicity over complexity

Security over convenience

No secrets in repo

Reproducible modules

Public metadata only
