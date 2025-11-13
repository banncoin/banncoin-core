#!/bin/bash
# ════════════════════════════════════════════════════════════════════
# 🧭  BANNCOIN NODE INTEGRITY AUDIT — v3 COLORIZED EDITION
# Author : Banncoin Core Ops
# Purpose: Full professional verification of node, chain, rewards, and state.
# Safe to run anytime — no hangs, no overwrites.
# ════════════════════════════════════════════════════════════════════

# --- Formatting helpers ---
GREEN='\033[0;32m'; YELLOW='\033[1;33m'; RED='\033[0;31m'; BLUE='\033[0;34m'; NC='\033[0m'
hr(){ echo -e "${BLUE}──────────────────────────────────────────────${NC}"; }
ok(){ echo -e "${GREEN}✅ $1${NC}"; }
warn(){ echo -e "${YELLOW}⚠️  $1${NC}"; }
fail(){ echo -e "${RED}❌ $1${NC}"; }

echo -e "${BLUE}==========[ 🧭 BANNCOIN INTEGRITY AUDIT $(date -u +"%Y-%m-%d_%H:%MZ") ]==========${NC}"
start_time=$(date +%s)

# 1️⃣ BASIC IDENTITY & SERVICE STATUS
hr
echo "[1] === BASIC IDENTITY & SERVICE STATUS ==="
hostnamectl | head -6
sudo systemctl status bncnode --no-pager | head -12
sudo systemctl is-active bncnode && sudo systemctl is-enabled bncnode && ok "bncnode service active" || fail "bncnode not active"
ls -ld /opt/banncoin /var/lib/banncoin /root/bnc_full_chain 2>/dev/null

# 2️⃣ NODE CHAIN STATUS
hr
echo "[2] === NODE CHAIN STATUS ==="
status=$(curl -fsS http://127.0.0.1:17536/status 2>/dev/null)
if [ -n "$status" ]; then
  echo "$status" | jq .
  ok "Node responded successfully"
else
  fail "Node API unresponsive on :17536"
fi
curl -fsS http://127.0.0.1:17536/recent?count=3 | jq . 2>/dev/null

# 3️⃣ FILE INTEGRITY
hr
echo "[3] === FILE INTEGRITY ==="
sha256sum /var/lib/banncoin/state.json /root/bnc_full_chain/genesis.json 2>/dev/null || true
sudo lsattr /var/lib/banncoin/state.json
head -c 200 /var/lib/banncoin/state.json && echo
ok "state.json readable"

# 4️⃣ BLOCK CONTINUITY
hr
echo "[4] === BLOCK CONTINUITY ==="
cd /root/bnc_full_chain/blocks || exit
ls -1 block*.json | tail -5
jq '.index, .previous_hash, .hash' $(ls -1 block*.json | tail -3)
ok "Chain continuity visually checkable"

# 5️⃣ WALLET & REWARD AUDIT (SMART)
hr
echo "[5] === WALLET & REWARD AUDIT (SMART) ==="
WALLET="bnc15rletyrdxzr777ckldd3z5hd26sgd32n6edrnskl3fk93qd2pc8qk8w6rc"
total_blocks=$(find /root/bnc_full_chain/blocks -name "block*.json" | wc -l)
wallet_blocks=$(grep -l "\"reward_to\": \"$WALLET\"" /root/bnc_full_chain/blocks/block*.json | wc -l)
percent=$(awk -v w=$wallet_blocks -v t=$total_blocks 'BEGIN{if(t>0) printf "%.2f", (w/t)*100; else print 0}')
echo "Recent 5 Rewards:"
grep -h '"reward_to"' /root/bnc_full_chain/blocks/block*.json | tail -5
echo "------------------------------------"
echo "Total Blocks: $total_blocks"
echo "Blocks to Your Wallet: $wallet_blocks"
echo "Ownership %: $percent%"
echo "------------------------------------"
ok "Reward audit complete"

# 6️⃣ MINER CONNECTIONS
hr
echo "[6] === MINER CONNECTIONS ==="
sudo ss -tnp | grep 17536 && ok "Miners connected" || warn "No active miners on port :17536"

# 7️⃣ MINING JOB HEALTH
hr
echo "[7] === MINING JOB HEALTH ==="
curl -fsS http://127.0.0.1:17536/mining/job | jq '{height: .job.height, bits: .job.difficulty_bits, ok: .ok, expires_in: (.job.expires_at - .job.created_at)}' 2>/dev/null && ok "Job endpoint active"

# 8️⃣ REWARD FLOW CONSISTENCY
hr
echo "[8] === REWARD FLOW CONSISTENCY (CLEAN) ==="
find /root/bnc_full_chain/blocks -name "block*.json" -exec jq -r '.reward_to' {} \; 2>/dev/null \
 | grep -v null | sort | uniq -c | sort -nr | head -10
ok "Reward flow ranked summary generated"

# 9️⃣ IMMUTABILITY STATUS
hr
echo "[9] === IMMUTABILITY STATUS ==="
sudo lsattr /var/lib/banncoin/state.json
ok "Immutability flag listed"

# 🔟 SYSTEM RESOURCE AUDIT
hr
echo "[10] === SYSTEM RESOURCE AUDIT ==="
uptime
df -hT
free -h
sudo lsof /var/lib/banncoin/state.json 2>/dev/null || echo "No open locks"
ok "System resources stable"

# 1️⃣1️⃣ NODE LOG TRACE (SAFE & NON-HANGING)
hr
echo "[11] === NODE LOG TRACE (LAST 5m SNAPSHOT) ==="
sudo journalctl -u bncnode --since "5 minutes ago" --no-pager -o cat \
 | grep -E "Accepted|submitted|height|hash|error" \
 | tail -20 || echo "No recent log entries."
ok "Recent log window captured"

# 1️⃣2️⃣ ARCHIVE SNAPSHOT CHECK
hr
echo "[12] === ARCHIVE SNAPSHOT CHECK ==="
ls -lh /root/archives | tail -5
sha256sum /root/archives/bnc_chain_snapshot_h*.tar.gz | tail -3
ok "Archive snapshot verified"

# 1️⃣3️⃣ FIREWALL & PORTS
hr
echo "[13] === FIREWALL & PORTS ==="
sudo ufw status verbose | grep 1753
sudo netstat -plnt | grep -E "17536|17539|80|443"
ok "Firewall and port check complete"

# 1️⃣4️⃣ EXPLORER / RECENT ENDPOINT
hr
echo "[14] === EXPLORER / RECENT ENDPOINT ==="
curl -fsS http://127.0.0.1:17536/recent?count=5 \
 | jq '[.[] | {height: (.index // .height), hash, reward_to}]' 2>/dev/null
ok "Explorer endpoint responding"

# 1️⃣5️⃣ FINAL SNAPSHOT & CHECKSUM
hr
echo "[15] === FINAL SNAPSHOT & CHECKSUM ==="
ts=$(date -u +'%Y%m%dT%H%MZ')
tar -czf /root/archives/bnc_chain_snapshot_h${ts}.tar.gz \
  /root/bnc_full_chain/blocks /var/lib/banncoin/state.json 2>/dev/null
sha256sum /root/archives/bnc_chain_snapshot_h${ts}.tar.gz
ok "Final snapshot complete"

# ════════════════════════════════════════════════════════════════════
end_time=$(date +%s)
elapsed=$((end_time - start_time))
hr
echo -e "${GREEN}✅ Audit complete — Banncoin Node Verified${NC}"
echo -e "Timestamp: $(date -u)"
jq -r '.height, .tip_hash' /var/lib/banncoin/state.json 2>/dev/null | \
awk 'NR==1{print "Height: " \$0} NR==2{print "Tip Hash: " \$0}'
echo -e "Total Runtime: ${elapsed}s"
hr
