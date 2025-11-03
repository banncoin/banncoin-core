import json, datetime, os

data = {
    "height": 40277,           # example placeholder
    "difficulty_bits": 24,
    "hash": "00000abc...xyz",
    "ok": True,
    "exported_at": datetime.datetime.utcnow().isoformat() + "Z"
}

out = os.path.expanduser("~/Banncoin_GitHub_Backup/site/docs/status.json")
with open(out, "w") as f:
    json.dump(data, f, indent=2)
