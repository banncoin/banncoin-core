# Banncoin Mining Guide (Developer Edition)

This document explains how to run the official Banncoin Harmonic Miner (v5.x)
using the public node API at:

https://node.banncoin.org

yaml
Copy code

Mining is fully open and permissionless in **Era B**.

---

## 1. Requirements

- Python **3.8 or later**
- Linux, macOS, or Windows (WSL2 recommended)
- A Banncoin wallet
- Internet access to the public node API

Generate a wallet using the offline generator on Banncoin.org.

---

## 2. Example Wallet Address

This guide uses the example address:

bnc15rletyrdxzr777ckldd3z5hd26sgd32n6edrnskl3fk93qd2pc8qk8w6rc

yaml
Copy code

Replace this with your own wallet when mining.

---

## 3. Clone the Public Miner

```bash
git clone https://github.com/banncoin/banncoin-core.git
cd banncoin-core/miner
cp bnc_miner.py ~/bnc_miner.py
mkdir -p ~/miner_logs
You now have the official miner at:

bash
Copy code
~/bnc_miner.py
4. Start Mining
bash
Copy code
python3 ~/bnc_miner.py \
  --api https://node.banncoin.org \
  --reward-to YOUR_WALLET \
  --log-dir ~/miner_logs
The miner automatically:

Fetches difficulty

Builds the next block template

Searches for a valid nonce

Submits accepted blocks to the Banncoin network

A successful block shows:

json
Copy code
{"status":"accepted"}
5. Check Current Chain Status
Visit:

arduino
Copy code
https://node.banncoin.org/status
6. Running the Miner in Background (systemd)
For VPS or dedicated miners, create:

/etc/systemd/system/bnc-miner.service

ini
Copy code
[Unit]
Description=Banncoin Miner
After=network.target

[Service]
Type=simple
User=YOURUSER
WorkingDirectory=/home/YOURUSER
ExecStart=/usr/bin/python3 /home/YOURUSER/bnc_miner.py \
  --api https://node.banncoin.org \
  --reward-to YOUR_WALLET \
  --sleep 0.5 \
  --log-dir /home/YOURUSER/miner_logs
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
Enable:

bash
Copy code
sudo systemctl daemon-reload
sudo systemctl enable --now bnc-miner.service
7. Troubleshooting
Miner exits immediately
Python < 3.8 — upgrade Python.

No accepted blocks
Difficulty varies. Ensure system is not overloaded.

Miner stops when laptop sleeps
Disable OS sleep, or use a VPS miner.

8. License & Contribution
See the repository root for license, contributing rules, and security policy.

Banncoin — Sovereign, Open, Permissionless.

yaml
Copy code

---
