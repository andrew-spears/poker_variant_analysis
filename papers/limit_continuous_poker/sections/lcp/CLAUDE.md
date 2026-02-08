# LCP Section

## Purpose
Formally defines Limit Continuous Poker (LCP) - the main game variant studied in the paper.

## Key Content

### Game Definition
- Two players: bettor and caller
- Hand strengths X, Y ~ Uniform[0,1], independent
- Bettor's actions: check (0) or bet s in [L, U]
- Caller's actions (if bettor bets): call or fold

### Payoff Structure
- Check: +0.5 to higher hand
- Bet s, caller calls: +0.5 + 2s to higher hand
- Bet s, caller folds: +0.5 to bettor

### Strategy Spaces
- Bettor: measurable function σ₁: [0,1] → {0} ∪ [L,U]
- Caller: measurable function σ₂: [L,U] × [0,1] → {call, fold}

### Motivation
1. **Realism**: Real poker has bet constraints (stack sizes, minimum bets)
2. **Generalization**:
   - L→0, U→∞: LCP → NLCP
   - L→B, U→B: LCP → FBCP

## Key Parameters
- L: minimum bet size
- U: maximum bet size

## Forward References
- Section on solving LCP (methodology)
- Section on Nash equilibrium structure
- Section on strategic convergence (formal limit proofs)
