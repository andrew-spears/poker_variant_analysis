# Game Value Section

## Purpose
Analyzes the expected payoff (game value) of LCP and proves key properties.

## Key Content

### Main Result (Theorem)
Game value formula:

V_LCP(L, U) = [(1+L)³(1+U)³ - ((1+L)³ + L³(1+U)³)] / [14(1+L)³(1+U)³ - 2((1+L)³ + L³(1+U)³)]

In (r,t) coordinates:
**V(r, t) = (1 - r³ - t³) / (14 - 2r³ - 2t³)**

### Symmetry Property
V(r, t) = V(t, r)
Equivalently: V_LCP(L, U) = V_LCP(1/U, 1/L)

Interpretation: Swapping min/max bet constraints (reciprocally around pot size 1) preserves game value.

### Parameter Interpretation
- r = L/(1+L): minimum pot odds (caller's best case)
- t = 1/(1+U): pot fraction at max bet
- Small r: min bet negligible
- Small t: max bet very large

### Monotonicity
- ∂V/∂U >= 0 (more max flexibility helps bettor)
- ∂V/∂L <= 0 (higher min hurts bettor)

Proof uses chain rule with (r,t) derivatives.

### Convergence
- As L,U → B: V → V_FB(B) = B/[2(1+2B)(2+B)]
- As L→0, U→∞: V → V_NL = 1/14

## Images
- `images/game_value_plots.png` - Value function visualization
- `images/game_value_rt.png` - Value in (r,t) coordinates

## Dependencies
- Nash equilibrium section (for strategy profile)
- Appendix for full value computation
