#!/bin/bash
# 🧊 Banncoin Cold Sync — Pi / Archive Node Edition
# © 2025 Banncoin. All rights reserved.

timestamp=$(date -u +'%Y-%m-%dT%H:%MZ')
log_root="$HOME/logs"
backup_root="/mnt/banncoin_backup/$timestamp"

echo "=== 🧊 Banncoin Cold Sync @ $timestamp ==="
mkdir -p "$log_root" "$backup_root/live" "$backup_root/node_archives"

echo "→ Syncing live site files..."
rsync -a --delete "$HOME/bnc_full_chain/" "$backup_root/live/" >> "$log_root/cold_sync_history.log" 2>&1

echo "→ Pulling archives from node (if reachable)..."
ssh -o ConnectTimeout=5 root@node.banncoin.org "tar -czf - /root/archives" \
    | tar -xzf - -C "$backup_root/node_archives/" 2>>"$log_root/cold_sync_history.log" \
    || echo "⚠️ Node unreachable — skipped" >> "$log_root/cold_sync_history.log"

echo "[${timestamp}] ✅ Cold backup complete — Live+Node synced" >> "$log_root/cold_sync_history.log"
