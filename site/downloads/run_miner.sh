#!/usr/bin/env bash
set -e
NODE="node.banncoin.org:17536"
WALLET="$1"
if [ -z "$WALLET" ]; then
  read -rp "Enter your BNC address (bnc1...): " WALLET
fi
# curl then run
curl -fsSL https://banncoin.org/downloads/banncoin_miner.py -o banncoin_miner.py
python3 banncoin_miner.py --node "$NODE" --wallet "$WALLET"
