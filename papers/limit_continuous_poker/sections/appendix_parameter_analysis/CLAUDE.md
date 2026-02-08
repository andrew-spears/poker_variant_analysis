# Appendix: Parameter Analysis Proofs

## Purpose
Complete proofs for how parameters L and U affect equilibrium strategies and payoffs.

## Key Content

### Same content as parameter_analysis section, but designated as appendix material.

The main body (summary_analysis) references these proofs.

### Key Results Proven

**Theorem (Payoff Increasing Threshold)**
dEV(x)/dU < 0 if x < max(v(U), threshold)
dEV(x)/dU > 0 otherwise

**Lemma: x₂ Increasing in U**
dx₂/dU = 18t²/[(1+U)²(r³+t³-7)²] > 0

**Lemma: v^(-1)(x) Decreasing in U**
For x in [x₃, v(U)]:
d/dU v^(-1)(x) = (∂v^(-1)/∂x₂)(∂x₂/∂t)(dt/dU) < 0

**Lemma: c(v^(-1)(x)) Increasing in U**
Despite smaller bets, calling cutoff increases.
Two effects: direct (through x₂) and indirect (through bet size).
Direct effect dominates.

### Proof of Main Theorem
**Case 1 (x > v(U))**: Uses multivariate chain rule on EV at s=U. Threshold for sign change derived.

**Case 2 (x in [x₃, v(U)])**: Both terms in dEV/dU are negative (product of opposite-sign factors).

## Images
- References ev_vs_U.png

## Dependencies
- Nash equilibrium formulas
- Payoff analysis EV expressions
