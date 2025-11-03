#!/usr/bin/env python3
# Simple Banncoin CPU miner (Windows/Mac/Linux)
# - Canonical header order to match node
# - Half-gate when target=5 (submit only if next nibble < 8) ≈ 30–35s
# - Periodic job refresh so we don't grind stale target=8 jobs

import argparse, json, socket, time, hashlib, random

def rpc(host, port, msg):
    s = socket.socket()
    s.connect((host, port))
    s.send((json.dumps(msg) + "\n").encode())
    data = s.recv(4096)
    s.close()
    return json.loads(data.decode())

def canonical_header(h):
    return {
        "height":         int(h["height"]),
        "prev":           str(h["prev"]),
        "merkle":         str(h["merkle"]),
        "timestamp":      int(h["timestamp"]),
        "target_prefix":  int(h["target_prefix"]),
        "wallet":         str(h["wallet"]),
        "nonce":          int(h["nonce"]),
    }

def header_hash(h):
    js = json.dumps(canonical_header(h), separators=(",",":"), ensure_ascii=False).encode()
    return hashlib.sha256(js).hexdigest()

def mine(host, port, wallet):
    while True:
        # fetch a fresh job
        job = rpc(host, port, {"type": "get_mining_job", "wallet": wallet})
        height        = int(job["height"])
        target_prefix = int(job["target_prefix"])
        prefix        = "0" * target_prefix

        # half-gate for target=5 (keep consensus at 5, throttle submissions a bit)
        nibble_limit  = 8 if target_prefix == 5 else 16

        # refresh job periodically to avoid grinding temporary 8s
        job_started   = time.time()
        job_ttl_sec   = 12

        base = {
            "height":        height,
            "prev":          job["prev_hash"],
            "merkle":        job["merkle_root"],
            "timestamp":     int(job["timestamp"]),   # node will re-stamp on accept
            "target_prefix": target_prefix,
            "wallet":        wallet,
        }

        print(f"[job] height={height} target={target_prefix} prev={base['prev'][:8]}..")
        nonce = random.randrange(0, 1 << 31)
        tries = 0
        t0    = time.time()

        while True:
            hdr = base.copy()
            hdr["nonce"] = nonce
            hh = header_hash(hdr)

            if hh.startswith(prefix) and int(hh[target_prefix], 16) < nibble_limit:
                submit = {
                    "height":        int(hdr["height"]),
                    "prev_hash":     str(hdr["prev"]),
                    "merkle_root":   str(hdr["merkle"]),
                    "timestamp":     int(hdr["timestamp"]),
                    "target_prefix": int(hdr["target_prefix"]),
                    "wallet":        str(hdr["wallet"]),
                    "nonce":         int(hdr["nonce"]),
                    "block_hash":    hh,
                }
                res = rpc(host, port, {"type": "submit_block", **submit})
                print(f"[submit] {res}")
                break

            tries += 1
            if tries % 100000 == 0:
                elapsed = time.time() - t0
                if elapsed > 0:
                    rate = int(tries / elapsed)
                    print(f"[{height}] {rate} H/s  nonce={nonce}")
                t0 = time.time()
                tries = 0

            if time.time() - job_started > job_ttl_sec:
                print("[job] refresh")
                break

            nonce = (nonce + 1) & 0x7fffffff

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--node", default="node.banncoin.org:17536", help="host:port of a Banncoin node")
    ap.add_argument("--wallet", required=True, help="your bnc1... address")
    args = ap.parse_args()
    host, port = args.node.split(":")
    mine(host, int(port), args.wallet)
