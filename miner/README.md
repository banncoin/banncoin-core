🜂 Banncoin Miner — Remote API Edition

A field-forged worker of the Bannchain — listening for sovereign signals, shaping valid blocks, and returning earned tribute to its keeper.

⚠️ IMPORTANT — DO NOT mine to placeholders like YOUR_WALLET.
Always replace with your real Banncoin address (bnc1…).
Never put quotes around the address.
If you mine to literal placeholders, your reward will be lost to the void (lol).

⚡ QUICKSTART

python3 bnc_miner.py
--api https://node.banncoin.org

--reward-to YOUR_WALLET
--sleep 0.1
--log-dir ./miner_logs

🏛 Known Founding Addresses (Public)

These Banncoin addresses were used during early Bannchain mining + testing.
They are shared for transparency & chain archaeology.

⚠️ You can mine to these, but it is NOT recommended since rewards won't belong to you.

bnc15rletyrdxzr777ckldd3z5hd26sgd32n6edrnskl3fk93qd2pc8qk8w6rc
bnc1tu70vzq0fz85zaxz04zycgvkun288efel7jhes76rkzq6m08lxfs4tm8wn

Choose your own destiny — but choose your own address.
The chain favors sovereign hands.

🔧 CLI FLAGS

--api Banncoin node endpoint
--reward-to Your BNC wallet address
--sleep Delay between nonce batches
--log-dir Path for miner log files

📦 Requirements

pip3 install -r requirements.txt --break-system-packages

Dependencies:
requests>=2.31.0

Genesis Codex

"Value grows where no master can touch."
