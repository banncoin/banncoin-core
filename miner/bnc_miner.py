#!/usr/bin/env python3
import argparse
import hashlib
import json
import os
import time
import requests
import logging
from datetime import datetime, timezone
from requests.exceptions import RequestException

# ==============================================================
# ⚒️  Banncoin Harmonic Miner — Remote API Edition (v5.2)
#  Clean logging for non-root environments
# ==============================================================

REWARD_PER_BLOCK = 458
DEFAULT_API = "https://api.banncoin.org"
DEFAULT_LOGFILE = "/var/log/banncoin/miner.log"

# --------------------------------------------------------------
# Utility helpers
# --------------------------------------------------------------
def now_iso():
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

def dsha256(b): return hashlib.sha256(hashlib.sha256(b).digest()).digest()
def sha256_hex(b): return hashlib.sha256(b).hexdigest()

def little_u32(n): return int(n & 0xFFFFFFFF).to_bytes(4, "little")
def little_u64(n): return int(n & 0xFFFFFFFFFFFFFFFF).to_bytes(8, "little")

def header_bytes(block):
    return (
        little_u32(block["version"]) +
        bytes.fromhex(block["prev_hash"]) +
        bytes.fromhex(block["merkle_root"]) +
        block["timestamp"].encode() +
        little_u32(block["difficulty_bits"]) +
        little_u64(block["nonce"])
    )

def target_prefix(bits): return "0" * (bits // 4)

# --------------------------------------------------------------
# Node interface
# --------------------------------------------------------------
def get_status(api):
    r = requests.get(f"{api}/status", timeout=8)
    r.raise_for_status()
    return r.json()

def get_tip(api):
    s = get_status(api)
    return s.get("height", 0), s.get("hash", ""), s.get("difficulty_bits", 10)

def submit_block(api, block):
    try:
        r = requests.post(f"{api}/submit_block", json=block, timeout=10)
        try:
            return r.status_code, r.json()
        except Exception:
            return r.status_code, {"raw": r.text}
    except RequestException as e:
        return None, {"error": str(e)}

# --------------------------------------------------------------
# Logging setup
# --------------------------------------------------------------
def setup_logging():
    try:
        os.makedirs(os.path.dirname(DEFAULT_LOGFILE), exist_ok=True)
        logging.basicConfig(
            filename=DEFAULT_LOGFILE,
            level=logging.INFO,
            format="%(asctime)s [%(levelname)s] %(message)s",
        )
    except PermissionError:
        # Fallback to stdout if file unwritable
        logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
        logging.warning(f"⚠️ Cannot write {DEFAULT_LOGFILE}; logging to stdout.")

# --------------------------------------------------------------
# Wallet helpers
# --------------------------------------------------------------
def ensure_logs(dirpath):
    os.makedirs(dirpath, exist_ok=True)
    csv_path = os.path.join(dirpath, "blocks.csv")
    ndjson_path = os.path.join(dirpath, "events.ndjson")
    if not os.path.exists(csv_path):
        with open(csv_path, "w", newline="") as f:
            f.write("ts,index,height,bits,nonce,elapsed_s,hashrate_hps,status,hash,reward_to\n")
    if not os.path.exists(ndjson_path):
        open(ndjson_path, "a").close()
    return csv_path, ndjson_path

def append_csv(path, row):
    with open(path, "a", newline="") as f:
        f.write(row + "\n")

def append_ndjson(path, obj):
    with open(path, "a") as f:
        f.write(json.dumps(obj, separators=(",", ":")) + "\n")

def ensure_wallet_totals(dirpath):
    os.makedirs(dirpath, exist_ok=True)
    path = os.path.join(dirpath, "wallet_totals.csv")
    if not os.path.exists(path):
        with open(path, "w", newline="") as f:
            f.write("ts,wallet,reward,total\n")
    return path

def load_wallet_totals_cache(path):
    cache = {}
    if not os.path.exists(path): return cache
    with open(path, "r") as f:
        next(f, None)
        for line in f:
            parts = line.strip().split(",")
            if len(parts) >= 4:
                cache[parts[1]] = int(parts[3])
    return cache

def bump_wallet_total(path, cache, wallet, reward):
    total = cache.get(wallet, 0) + reward
    cache[wallet] = total
    with open(path, "a", newline="") as f:
        f.write(f"{now_iso()},{wallet},{reward},{total}\n")
    return total

# --------------------------------------------------------------
# Mining logic
# --------------------------------------------------------------
def main():
    p = argparse.ArgumentParser(description="Banncoin Miner — Remote API Edition")
    p.add_argument("--api", default=DEFAULT_API)
    p.add_argument("--reward-to", required=True)
    p.add_argument("--sleep", type=float, default=0.0)
    p.add_argument("--log-dir", default="/home/banncoin/miner_logs")
    args = p.parse_args()

    setup_logging()
    logging.info("⧖ Sovereign Pulse Detected — Bann Field Coherence Stabilizing…")
    logging.info(f"Miner start | api={args.api} | logs={args.log_dir}")

    csv_path, ndjson_path = ensure_logs(args.log_dir)
    totals_path = ensure_wallet_totals(args.log_dir)
    totals_cache = load_wallet_totals_cache(totals_path)

    total_hashes, start_wall = 0, time.time()
    while True:
        try:
            height, tip, bits = get_tip(args.api)
        except Exception as e:
            logging.error(f"Node unreachable: {e}")
            time.sleep(3)
            continue

        merkle = sha256_hex(f"{args.reward_to}:{REWARD_PER_BLOCK}:{height+1}".encode())
        block = {
            "index": height + 1, "version": 1, "prev_hash": tip,
            "merkle_root": merkle, "timestamp": now_iso(),
            "difficulty_bits": bits, "nonce": 0,
            "hash": "", "reward": REWARD_PER_BLOCK,
            "reward_to": args.reward_to,
        }

        t_pref = target_prefix(bits)
        start, tried, best = time.time(), 0, None
        logging.info(f"⛏️  Mining block {block['index']} bits={bits} target≈{t_pref}")

        while True:
            h = dsha256(header_bytes(block)).hex()
            if best is None or h < best:
                best = h
            if h.startswith(t_pref):
                elapsed = time.time() - start
                hps = tried / elapsed if elapsed else 0
                code, resp = submit_block(args.api, {**block, "hash": h})
                status = "accepted" if code == 200 else "error"
                logging.info(f"[✓] SOLVED nonce={block['nonce']} {status.upper()} code={code}")
                if status == "accepted":
                    new_total = bump_wallet_total(totals_path, totals_cache, args.reward_to, REWARD_PER_BLOCK)
                    logging.info(f"[wallet] {args.reward_to} +{REWARD_PER_BLOCK} → {new_total} BNC")
                append_csv(csv_path, f"{now_iso()},{block['index']},{height},{bits},{block['nonce']},{elapsed:.2f},{hps:.2f},{status},{h},{args.reward_to}")
                append_ndjson(ndjson_path, {"ts": now_iso(), "hash": h, "status": status})
                break
            block["nonce"] += 1
            tried += 1
            total_hashes += 1
            if tried % 100000 == 0:
                elapsed = time.time() - start
                hps = tried / elapsed if elapsed else 0
                logging.info(f"progress {tried:,} ~{int(hps):,}/s best={best[:12]}…")
            if args.sleep > 0:
                time.sleep(args.sleep)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        logging.info("[halt] Miner stopped by user")
