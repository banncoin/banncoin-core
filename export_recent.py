import json, datetime, os

data = {
    "exported_at": datetime.datetime.utcnow().isoformat() + "Z",
    "ok": True,
    "recent_blocks": [
        {"index": 40275, "timestamp": "2025-11-03T10:05Z",
         "hash": "000004...", "previous_hash": "000005...",
         "difficulty_bits": 24, "reward_to": "bnc1...", "nonce": 320003}
    ]
}

out = os.path.expanduser("~/Banncoin_GitHub_Backup/site/docs/recent.json")
with open(out, "w") as f:
    json.dump(data, f, indent=2)
