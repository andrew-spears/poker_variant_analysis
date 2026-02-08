# Appendix: Nash Equilibrium Proof

## Purpose
Rigorous verification that the strategy profile from Section 4 constitutes a Nash equilibrium.

## Key Content

### Proof Structure
Show no player can improve by unilateral deviation.

### Caller's Deviation Analysis
For any bet size s and hand y:
- E[call | y, s] = P[x < y | s](1+s) + P[x >= y | s](-s)
- E[fold | y, s] = 0

At y = c(s): indifferent by design.
E[call] increasing in y, so:
- y > c(s): calling weakly better
- y < c(s): folding weakly better

### Bettor's Deviation Analysis (5 Cases)

**Case 1: x < c(s) (potential bluffs)**
- E[bet s | x] = c(s) - (1-c(s))s = x₂ (constant, independent of x)
- E[check | x] = x
- Indifferent at x = x₂
- Bet preferable for x < x₂, check for x₂ < x < c(L)

**Case 2: c(s) <= x < x₃ (could value bet, should check)**
- E[bet s | x] = s(2x - c(s) - 1) + x
- From indifference condition: 2x - c(s) - 1 <= 0
- Therefore E[bet] <= E[check] = x

**Case 3: x₃ <= x < x₄ (min value bet)**
- E[bet L | x] >= E[check | x] (verified)
- E[bet s | x] decreasing in s for x < x₄
- Min bet optimal

**Case 4: x₄ <= x < x₅ (intermediate value bet)**
- E[bet L | x] >= E[check | x]
- dE/ds = 0 at s = v^(-1)(x) by optimality condition
- E increasing for s < v^(-1)(x), decreasing for s > v^(-1)(x)
- Optimal bet is v^(-1)(x)

**Case 5: x₅ <= x <= 1 (max value bet)**
- E increasing in s for x > x₅
- Max bet U optimal

## Figures
- TikZ diagram showing caller threshold decision

## Technical Notes
- Solution obtained via Mathematica symbolic solver
- See Appendix C for Mathematica code
