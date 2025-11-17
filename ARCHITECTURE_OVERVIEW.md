# Banncoin Architecture Overview

## 1. Chain Eras
- **Era A — Pre-economic bootstrap (0 → 33238)**
  - Rewards exist but are not spendable
  - Genesis foundation only
- **Era B — Economic mining (33239 → ∞)**
  - All rewards valid and transferable

## 2. System Components
### Node
Maintains chain state, validates blocks, adjusts difficulty, exposes API.

### Miner
CPU harmonic miner:
- Pulls template  
- Generates nonces  
- Submits solved blocks  
- Obeys dynamic difficulty  

### Integrity Audit
Reference script verifying:
- Chain continuity  
- Era boundaries  
- Reward distribution  
- Snapshot correctness  

## 3. Immutability Rules
- Genesis is frozen  
- Era A is frozen  
- Era B rules cannot retroactively modify past blocks  

## 4. API Endpoints
- `/status` — chain difficulty, tip  
- `/recent` — last 100 blocks  
- `/manifest.json` — chain metadata
