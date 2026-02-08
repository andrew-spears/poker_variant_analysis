# Solving LCP Section

## Purpose
Develops the methodology for computing Nash equilibrium - establishes equilibrium selection criteria and derives the constraint equations.

## Key Content

### Equilibrium Selection
LCP has infinitely many equilibria. Two refinements select unique solution:
1. Caller uses monotone strategies
2. Bettor's strategy is monotone-admissible

### Monotone Calling Strategies (Definition)
1. For fixed bet s: stronger hands more likely to call
2. For fixed hand y: smaller bets more likely to be called

Condition 1 is dominated if violated (proven in Appendix).
Condition 2 prevents exploitation (not dominated, but weaker).

### Monotone-Admissible Strategy
Betting strategy admissible against all monotone calling strategies.
Distinguishes how bettor bluffs: weaker hands bluff larger.

### Nash Equilibrium Structure
- Caller: threshold c(s), calls if y >= c(s)
- Bettor partitions [0,1] into:
  - Bluffing: [0, x₂] with sub-regions [0,x₀], [x₀,x₁], [x₁,x₂]
  - Checking: [x₂, x₃]
  - Value betting: [x₃, 1] with sub-regions [x₃,x₄], [x₄,x₅], [x₅,1]
- Bet sizes: continuous decreasing b(s) for bluffs, increasing v(s) for value

### Constraint Equations

**Caller Indifference:**
- (x₂-x₁)(1+L) - (x₄-x₃)L = 0
- x₀(1+U) - (1-x₅)U = 0
- |b'(s)|(1+s) - |v'(s)|s = 0

**Bettor Indifference/Optimality:**
- -sc'(s) - c(s) + 2v(s) - 1 = 0 (value optimality)
- Value-check indifference at x₃
- Bluff-check indifference at x₂

**Continuity:**
- b(U)=x₀, b(L)=x₁, v(U)=x₅, v(L)=x₄

## Images
- `images/` may contain strategy profile diagrams

## Forward References
- Appendix for full Nash equilibrium proof
