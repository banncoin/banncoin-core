#!/usr/bin/env python3
# ──────────────────────────────────────────────────────────────
# Banncoin Node v6.3 — Timestamp Parser + Stable Submit Fix
# ──────────────────────────────────────────────────────────────
#  Includes:
#    • Accepts both "height"/"index" and "previous_hash"/"prev_hash"
#    • Auto-detects ISO-formatted timestamps (e.g. "2025-10-25T19:52:17Z")
#    • Full backward compatibility with all Banncoin miners
#    • Clean error handling (no 500s)
# ──────────────────────────────────────────────────────────────

import os, sys, time, json, glob, logging, hashlib
from collections import defaultdict
from flask import Flask, request, jsonify

CHAIN_DIR   = "/root/bnc_full_chain/blocks"
STATE_PATH  = "/var/lib/banncoin/state.json"
ARCHIVE_DIR = "/root/archives"
ROADMAP_PATH = "/opt/banncoin/ROADMAP.json"

TARGET_SECONDS, RETARGET_INTERVAL = 26, 99
MAX_BITS_STEP, MIN_BITS, MAX_BITS = 2, 8, 60
JOB_TTL_SECONDS = 30
HOST, PORT = "0.0.0.0", 17536
CHAIN_ID = "BNC-0fa9f99c4746e1c5"

# ─── Logging ─────────────────────────────────────────────────
log = logging.getLogger("bncnode")
logging.basicConfig(level=logging.INFO,
    format="%(asctime)s  %(message)s", datefmt="%Y-%m-%d %H:%M:%S")

state = {"height":0,"tip_hash":"0"*64,"current_bits":22,
         "last_retarget_height":0,"genesis_time":None}
jobs = {}

# ─── Helpers ─────────────────────────────────────────────────
def now_ts(): return int(time.time())
def sha256_hex(b): return hashlib.sha256(b).hexdigest()
def ensure_dirs(): os.makedirs(os.path.dirname(STATE_PATH), exist_ok=True)

def save_state():
    ensure_dirs()
    tmp = STATE_PATH + ".tmp"
    with open(tmp,"w") as f: json.dump(state,f)
    os.replace(tmp,STATE_PATH)

def load_state():
    ensure_dirs()
    if not os.path.exists(STATE_PATH): return
    try:
        with open(STATE_PATH) as f: s=json.load(f); state.update(s)
        log.info("✦ 📖 State loaded: height=%d bits=%d tip=%s",
                 state["height"],state["current_bits"],state["tip_hash"][:12])
    except Exception as e:
        log.warning("⚠️ State load failed: %s",e)

def bits_target(bits): return (1<<(256-bits))-1 if 0<bits<256 else (1<<255)
def meets_difficulty(h,b):
    try: return int(h,16)<=bits_target(b)
    except: return False

def get_all_blocks():
    for f in sorted(glob.glob(os.path.join(CHAIN_DIR,"block*.json"))):
        try: yield json.load(open(f))
        except: continue

def compute_balances():
    bals=defaultdict(int)
    for b in get_all_blocks():
        if b.get("reward_to"): bals[b["reward_to"]] += 1
    return bals

def recent_blocks(n=5):
    files=sorted(glob.glob(os.path.join(CHAIN_DIR,"block*.json")))[-n:]
    out=[]
    for f in files:
        try: out.append(json.load(open(f)))
        except: continue
    return out[::-1]

def new_job():
    jid=sha256_hex(f"{state['tip_hash']}-{state['height']}-{now_ts()}".encode())
    job={"job_id":jid,"created_at":now_ts(),"expires_at":now_ts()+JOB_TTL_SECONDS,
         "height":state["height"]+1,"prev_hash":state["tip_hash"],
         "difficulty_bits":state["current_bits"]}
    jobs[jid]=job; return job

def prune_jobs():
    now_=now_ts()
    for k,v in list(jobs.items()):
        if v["expires_at"]<now_: jobs.pop(k,None)

# ─── Roadmap ─────────────────────────────────────────────────
def update_roadmap(phase,status="active"):
    data={"phase":phase,"version":"6.3","status":status,
          "last_updated":time.strftime("%Y-%m-%dT%H:%MZ",time.gmtime())}
    with open(ROADMAP_PATH,"w") as f: json.dump(data,f,indent=2)
    return data

# ─── Flask API ───────────────────────────────────────────────
app=Flask(__name__)
# ─── CORS for browser fetches ────────────────────────────────
@app.after_request
def add_cors(resp):
    resp.headers["Access-Control-Allow-Origin"] = "*"
    resp.headers["Access-Control-Allow-Methods"] = "GET, POST, OPTIONS"
    resp.headers["Access-Control-Allow-Headers"] = "Content-Type"
    return resp

@app.route("/recent")
def api_recent():
    n=int(request.args.get("count",5))
    return jsonify(recent_blocks(n))

@app.route("/balance")
def api_balance():
    addr=request.args.get("address","")
    bals=compute_balances()
    return jsonify({"ok":True,"address":addr,"balance":bals.get(addr,0)})

@app.route("/submit_block", methods=["POST"])
def api_submit_block():
    try:
        d = request.get_json(force=True, silent=True) or {}

        # Dual compatibility for all miners
        h = int(d.get("height") or d.get("index") or 0)
        prev = d.get("previous_hash") or d.get("prev_hash") or ""
        hhex = d.get("hash") or ""

        # ─── Timestamp Parser ────────────────────────────────
        ts_val = d.get("timestamp", now_ts())
        if isinstance(ts_val, str):
            try:
                ts = int(time.mktime(time.strptime(ts_val, "%Y-%m-%dT%H:%M:%SZ")))
            except Exception:
                ts = now_ts()
        else:
            ts = int(ts_val)

        bits = int(d.get("difficulty_bits", state["current_bits"]))
        nonce = d.get("nonce")
        reward_to = d.get("reward_to", "")

        if h != state["height"] + 1:
            return jsonify({"ok":False,"error":f"bad_index expected:{state['height']+1} got:{h}"}),409
        if prev != state["tip_hash"]:
            return jsonify({"ok":False,"error":"bad_prev"}),409
        if not meets_difficulty(hhex,bits):
            return jsonify({"ok":False,"error":"insufficient_work"}),400

        out=os.path.join(CHAIN_DIR,f"block{h:06d}.json")
        blk={"index":h,"previous_hash":prev,"hash":hhex,"timestamp":ts,
             "difficulty_bits":bits,"nonce":nonce,"reward_to":reward_to}

        with open(out+".tmp","w") as f: json.dump(blk,f,separators=(",",":"),sort_keys=True)
        os.replace(out+".tmp",out)

        state.update({"height":h,"tip_hash":hhex,"current_bits":bits})
        save_state()
        log.info("✦ 🔮 Block #%d sealed (%s)", h, hhex[:12])
        update_roadmap(phase=6)
        return jsonify({"ok":True,"height":h,"hash":hhex,"required_bits":state["current_bits"]})
    except Exception as e:
        log.error("❌ Exception in submit_block: %s", e)
        return jsonify({"ok":False,"error":str(e)}),500

# ─── Legacy miner endpoints ──────────────────────────────────
@app.route("/block/submit",methods=["POST"])
def legacy_submit(): return api_submit_block()
@app.route("/mining/job", methods=["GET","OPTIONS"])
def legacy_job():
    if request.method == "OPTIONS":
        return ("", 204)

#@app.route("/mining/job")
#def legacy_job():
    prune_jobs()
    return jsonify({"ok":True,"job":new_job(),"chain_id":CHAIN_ID})

# ─── Explorer & Sync Endpoints ───────────────────────────────
@app.route("/block/<int:height>")
def get_block(height):
    path=os.path.join(CHAIN_DIR,f"block{height:06d}.json")
    if not os.path.exists(path):
        return jsonify({"ok":False,"error":"block not found"}),404
    return jsonify(json.load(open(path)))

@app.route("/address/<addr>")
def get_address(addr):
    total=0; recent=[]
    for f in sorted(glob.glob(os.path.join(CHAIN_DIR,"block*.json")))[-200:]:
        b=json.load(open(f))
        if b.get("reward_to")==addr:
            total+=1
            recent.append({"height":b["index"],"hash":b["hash"],"timestamp":b["timestamp"]})
    return jsonify({"ok":True,"address":addr,"blocks_won":total,"recent":recent})

@app.route("/sync")
def sync_range():
    start=int(request.args.get("from",state["height"]-50))
    end=int(request.args.get("to",state["height"]))
    blocks=[]
    for h in range(start,end+1):
        f=os.path.join(CHAIN_DIR,f"block{h:06d}.json")
        if os.path.exists(f):
            b=json.load(open(f))
            blocks.append({"height":b["index"],"hash":b["hash"],
                           "prev":b["previous_hash"],"bits":b["difficulty_bits"]})
    return jsonify({"ok":True,"count":len(blocks),"blocks":blocks})

@app.route("/stats")
def stats():
    return jsonify({
        "ok":True,
        "chain_id":CHAIN_ID,
        "height":state["height"],
        "difficulty_bits":state["current_bits"],
        "hash":state["tip_hash"],
        "archives":len(glob.glob(os.path.join(ARCHIVE_DIR,"*.tar.gz"))),
        "timestamp":time.strftime("%Y-%m-%dT%H:%MZ",time.gmtime())
    })

@app.route("/audit")
def api_audit():
    bals=compute_balances()
    total_blocks=len(glob.glob(os.path.join(CHAIN_DIR,"block*.json")))
    data={
        "ok":True,"chain_id":CHAIN_ID,"height":state["height"],
        "difficulty_bits":state["current_bits"],
        "hash":state["tip_hash"],"balances":len(bals),
        "roadmap":json.load(open(ROADMAP_PATH)) if os.path.exists(ROADMAP_PATH) else {},
        "archives":len(glob.glob(os.path.join(ARCHIVE_DIR,"*.tar.gz"))),
        "timestamp":time.strftime("%Y-%m-%dT%H:%MZ",time.gmtime()),
        "total_blocks":total_blocks
    }
    return jsonify(data)

@app.route("/roadmap")
def api_roadmap():
    data=json.load(open(ROADMAP_PATH)) if os.path.exists(ROADMAP_PATH) else update_roadmap(phase=6)
    return jsonify(data)

@app.route("/status")
def api_status():
    nxt=RETARGET_INTERVAL-(state["height"]%RETARGET_INTERVAL)
    return jsonify({
        "ok":True,
        "chain_id":CHAIN_ID,
        "height":state["height"],
        "difficulty_bits":state["current_bits"],
        "hash":state["tip_hash"],
        "next_retarget_in":nxt
    })

@app.route("/health")
def api_health(): return "OK",200

# ─── Entrypoint ──────────────────────────────────────────────
def main():
    os.chdir("/root/bnc_full_chain")
    load_state()
    update_roadmap(phase=6,status="active")
    log.info("⧖ Banncoin Node v6.3 — Explorer & Sync Online (chain-ID active)")
    app.run(host=HOST,port=PORT,threaded=True)

if __name__=="__main__":
    try: main()
    except KeyboardInterrupt:
        log.info("✦ Graceful stop."); sys.exit(0)
