# 🪙 Banncoin Core

<p align="center">
  <img src="https://raw.githubusercontent.com/banncoin/banncoin-core/main/site/assets/brand/banncoin-wordmark.svg" width="420">
</p>

<p align="center">
  <img src="https://img.shields.io/badge/license-Proprietary-blue">
  <img src="https://img.shields.io/badge/status-Active-success">
  <img src="https://img.shields.io/badge/chain-Mainnet-green">
  <img src="https://img.shields.io/badge/version-v1.0.0-lightgrey">
</p>

**Banks fail. Chains prevail.**  
Banncoin is a sovereign, miner-anchored blockchain protocol built to embody transparency, resilience, and self-governance.

---

## 🌐 Overview

This repository contains the **core Banncoin.org site bundle**, including:

| Folder | Purpose |
|-------|---------|
| `site/` | Public docs, JSON endpoints, and explorer mirrors |
| `node/` | Reference Banncoin node implementation |
| `miner/` | Harmonic CPU Miner |
| `scripts/` | Audits, snapshots, chain sync, automation |
| Root files (`index.html`, `status.json`, etc.) | Public chain metadata |

---

## ⚙️ Related Repositories

| Repository | Description |
|-----------|-------------|
| `banncoin-explorer` | Live chain view: blocks, miners, rewards |
| `banncoin-docs` | Documentation, governance, technical specs |
| **Private:** `banncoin-org` | Primary web bundle + Netlify deployment |
| **Private:** `banncoin-private` | Verified source archive & backups |

---

## ⛏️ Mining (Quick Overview)

The Harmonic Miner (CPU) is included in:

miner/bnc_miner.py

objectivec
Copy code

Quick-start CLI:

python3 bnc_miner.py --api https://node.banncoin.org
--reward-to bnc1YOUR_WALLET
--log-dir ./miner_logs

yaml
Copy code

Full guide:  
➡ `site/docs/mining.md`

---

## 🧰 Tech Stack

- **HTML / CSS / JS** — site & explorer
- **Python** — miner + node scripts
- **JSON** — chain metadata
- **GitHub + Netlify** — deployment & redundancy
- **Harmonic Chain Format** — block and reward logic

---

## 🪶 Chain Motto

> “Value grows where no master can touch.”

---

## 📦 License

© 2025 Banncoin. All rights reserved.  
See `LICENSE` for usage & redistribution guidelines.
