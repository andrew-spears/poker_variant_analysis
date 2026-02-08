# Appendix: Payoff Analysis Proofs

## Purpose
Complete proofs for expected value formulas and their properties.

## Key Content

### Theorem: Expected Value Formula
EV(x) piecewise defined over 5 regions:
1. Bluffing (x <= x₂): EV = x₂ - 1/2
2. Checking (x₂ < x <= x₃): EV = x - 1/2
3. Min value bet (x₃ < x < v(L)): EV = x(2L+1) - L(c(L)+1) - 1/2
4. Intermediate (v(L) <= x <= v(U)): EV = x(2v^(-1)(x)+1) - v^(-1)(x)(c(v^(-1)(x))+1) - 1/2
5. Max value bet (x > v(U)): EV = x(2U+1) - U(c(U)+1) - 1/2

### Proof of EV Formula
**Bluffing**: Hand strength irrelevant (never called by worse). By indifference at x₂, EV = x₂ - 1/2.

**Checking**: Win ante with probability x. EV = x - 1/2.

**Value betting**: Sum three outcomes:
- Fold: c(s) × 0.5
- Call worse: (x - c(s)) × (s + 0.5)
- Call better: (1 - x) × (-s - 0.5)

### Theorem: EV Monotonicity
EV(x) is increasing in x.

### Proof of Monotonicity
- Bluffing constant, checking linear increasing
- At x₃: indifferent, so continuous
- Min/max betting: dEV/dx = 2L+1 > 0, 2U+1 > 0
- Intermediate: Use chain rule + optimality condition dEV/ds = 0

### Strategic Discussion
Strongest hands accept low call frequency for large pots.
No slowplaying value (single round, no raising).
