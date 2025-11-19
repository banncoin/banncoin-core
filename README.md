# 🪙 Banncoin Core

![Banncoin Wordmark](https://raw.githubusercontent.com/banncoin/banncoin-core/main/site/assets/brand/banncoin-wordmark.svg)

[![License](https://img.shields.io/badge/license-Proprietary-blue)](LICENSE)
[![Status](https://img.shields.io/badge/status-Active-success)]()
[![Chain](https://img.shields.io/badge/chain-Mainnet-green)]()
[![Era](https://img.shields.io/badge/era-Era%20B-orange)]()
[![Miner](https://img.shields.io/badge/miner-v5.2-lightgrey)]()

**Banks fail. Chains prevail.**  
Banncoin is a sovereign, miner-anchored blockchain protocol built for transparency, resilience, and self-governance.

---

## 🌐 Overview

This repository contains the current **Banncoin Core** bundle:

| Folder      | Purpose                                      |
|:-----------|:----------------------------------------------|
| `site/`    | Public website, docs, and JSON endpoints      |
| `node/`    | Reference Banncoin node implementation        |
| `miner/`   | Banncoin Harmonic Miner (CPU)                 |
| `scripts/` | Automation, audits, and sync tooling          |

The live website is deployed separately from the private **`banncoin-org`** repo.

---

## ⚒️ Mining Quickstart (Developer View)

> 🔒 **Important:** Never mine to literal placeholders like `YOUR_WALLET`.  
> Always use a real Banncoin address starting with `bnc1…`.

Example command (using the **public founding example** wallet):

```bash
python3 bnc_miner.py \
  --api https://node.banncoin.org \
  --reward-to bnc15rletyrdxzr777ckldd3z5hd26sgd32n6edrnskl3fk93qd2pc8qk8w6rc \
  --log-dir ./miner_logs
This address is published for example and transparency only.

Replace it with your own Banncoin wallet when mining.

For a full end-user guide, see:

Website: https://banncoin.org/mining/

Developer doc: site/docs/mining.md (this repo)

📚 Documentation
Key public docs in this repo:

Mining guide: site/docs/mining.md

Status JSON: site/docs/status.json

Recent blocks JSON: site/docs/recent.json

Manifest / metadata: site/docs/manifest.json

Additional architecture notes:
ARCHITECTURE_OVERVIEW.md

🤝 Contributing
See CONTRIBUTING.md for:

Rules on secrets / IP hygiene

Expectations for miner and node changes

How to structure PRs and tests

Security issues: see SECURITY.md and email contact@banncoin.org.

🧰 Tech Stack
Python — node & miner

HTML / CSS / JS — site and docs

JSON — public chain metadata endpoints

GitHub + Netlify — deployment and redundancy for public assets

🪶 Motto
“Value grows where no master can touch.”

📦 License
© 2025 Banncoin. All rights reserved.
See LICENSE for usage and redistribution details.  
