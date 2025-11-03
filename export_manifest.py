import json, datetime, os

data = {
    "chain_id": "BNC-0fa9f99c4746e1c5",
    "genesis_hash": "000000...",
    "max_supply": 3333333333,
    "block_time_target": 26,
    "version": "v1.1.0-pre",
    "exported_at": datetime.datetime.utcnow().isoformat() + "Z"
}

out = os.path.expanduser("~/Banncoin_GitHub_Backup/site/docs/manifest.json")
with open(out, "w") as f:
    json.dump(data, f, indent=2)
