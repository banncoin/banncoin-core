# Banncoin Mining — Developer Guide (Era B)

Banncoin is a public, permissionless Proof-of-Work chain.  
Mining is fully active in **Era B**, meaning blocks pay spendable rewards and any CPU can join.

This document is for **developers, integrators, and contributors** working directly with the Banncoin Core repository.

---

## ⚡ Overview

Mining on Banncoin uses the lightweight **Harmonic Miner (v5.x)**.  
It is a single-file Python miner designed for:

- determinism  
- clarity of algorithm  
- cross-platform compatibility  
- transparent block template construction  
- clean rejection/acceptance handling  

The miner communicates with **any Banncoin node** exposing the `/mine` and `/submit` API endpoints.

---

## 🧱 Block Structure (Developer Summary)

A valid Banncoin block consists of:

| Field | Description |
|-------|-------------|
| `height` | Next chain height |
| `prev_hash` | Hash of previous block |
| `timestamp` | Unix milliseconds |
| `bits` | Difficulty target (compact) |
| `reward_to` | Bech32-style BNC1 address |
| `nonce` | 64-bit search space |
| `merkle_root` | Commitment for transactions / metadata |
| `hash` | Double-SHA256 of header |

The miner receives all template fields from the node **except the nonce**, which it searches locally.

---

## 🔧 Requirements

- Python **3.8+**
- Linux, macOS, or Windows via **WSL2**
- Stable network connection to a Banncoin node
- Your Banncoin wallet address  
  Example address (for documentation only):

bnc15rletyrdxzr777ckldd3z5hd26sgd32n6edrnskl3fk93qd2pc8qk8w6rc

yaml
Copy code

---

## 📦 Clone the Public Miner

git clone https://github.com/banncoin/banncoin-core.git
cd banncoin-core/miner
cp bnc_miner.py ~/bnc_miner.py
mkdir -p ~/miner_logs

yaml
Copy code

This keeps the miner in `~/bnc_miner.py` so users can update independently from the repo.

---

## ⛏️ Start Mining (Basic)

python3 ~/bnc_miner.py
--api https://node.banncoin.org
--reward-to YOUR_WALLET
--log-dir ~/miner_logs

yaml
Copy code

The miner will:

- request a fresh template
- compute target from `bits`
- scan the full nonce range
- submit the block when solved
- retry automatically on rejection or template change

---

## 📡 Public Community Node

The simplest public endpoint for miners and integrators:

https://node.banncoin.org

yaml
Copy code

Endpoints:

| HTTP Path | Purpose |
|----------|----------|
| `/status` | Chain/retarget information |
| `/mine` | Fetch block template |
| `/submit` | Submit solved block |
| `/recent` | Recent block metadata |
| `/live/stats.json` | Miner-friendly live stats |

---

## 🔒 Era A vs Era B (Developer Notes)

Banncoin defines:

- **Era A** — bootstrap era, rewards non-spendable  
- **Era B** — active economic era, rewards spendable

The miner automatically uses the correct reward logic once Era B height is reached.

---

## 🛠️ Run Miner as a System Service (Optional)

For VPS or 24/7 rigs:

sudo nano /etc/systemd/system/bnc-miner.service

makefile
Copy code

Paste:

[Unit]
Description=Banncoin Miner
After=network.target

[Service]
Type=simple
User=YOURUSER
WorkingDirectory=/home/YOURUSER
ExecStart=/usr/bin/python3 /home/YOURUSER/bnc_miner.py
--api https://node.banncoin.org
--reward-to YOUR_WALLET
--sleep 0.5
--log-dir /home/YOURUSER/miner_logs
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target

makefile
Copy code

Enable:

sudo systemctl daemon-reload
sudo systemctl enable --now bnc-miner.service

yaml
Copy code

---

## 🚀 Performance Notes (Developers)

- Banncoin blocks target ~**26 seconds** average.
- Difficulty retargets dynamically based on moving windows.
- Miner supports:
  - multi-template live updates  
  - rejection handling  
  - stale protection  
  - throttle (`--sleep`)  
  - log forwarding  

---

## 🔍 Troubleshooting

**Miner exits instantly**  
→ Ensure Python ≥ 3.8

**Low hashrate**  
→ Disable laptop power saving  
→ Close heavy applications  
→ Prefer Linux / WSL2 over Windows native Python

**Frequent stale blocks**  
→ Use `https://node.banncoin.org` or run your own node  
→ Ensure latency < 200ms

---

## 📚 Related Repos

| Repository | Purpose |
|-----------|---------|
| `banncoin-core` | Core protocol, node, miner |
| `banncoin-explorer` | Public chain explorer |
| `banncoin-org` | Official website & docs |

---

## 🏁 Summary

The Harmonic Miner is the canonical Banncoin PoW implementation:  
transparent, deterministic, auditable, and easy to extend.

Developers contributing improvements should follow:

- clean PRs  
- deterministic hashing  
- no side-channels  
- no external dependencies  

Banncoin is designed to be **sovereign, open, permissionless.**

“No value grows where no master can touch.”

yaml
Copy code

---

© 2025 Banncoin. Open mining. Open protocol.
