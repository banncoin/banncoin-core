# Contributing to Banncoin Core

Thank you for your interest in the Banncoin ecosystem.

## Repository Layout

site/ → Public documentation & API JSON
node/ → Banncoin Node (reference implementation)
miner/ → Harmonic Miner (CPU)
scripts/ → Automation, audits, sync tools

markdown
Copy code

## Rules

- No private IPs or environment details in commits  
- All changes must preserve deterministic chain behavior  
- Genesis, Era A and Era B are immutable  
- Mining logic must remain verifiable & CPU-fair  

## How to Contribute

1. Fork the repository  
2. Create a feature branch  
3. Submit a PR with a clear description  
4. Pass all smoke tests (`scripts/test-basic.sh`)  

## Documentation

Mining Guide  
→ `site/docs/mining.md`  
Node API  
→ `site/docs/status.json`, `site/docs/recent.json`  

For questions, open a discussion or contact maintainers.
