# Appendix: Monotone Strategy Proofs

## Purpose
Rigorous proofs about monotone calling strategies and their role in equilibrium uniqueness.

## Key Content

### Main Lemma
Non-monotone calling strategies are weakly dominated.

**Statement**: If caller violates first monotonicity condition (calls with A, folds with B where sup A <= inf B, both positive measure), the strategy is weakly dominated.

**Proof Technique**:
1. Find equal-measure subsets A' ⊆ A, B' ⊆ B (exists by nonatomic measure property)
2. Construct improved strategy σ_C' that swaps actions for A' and B'
3. Show σ_C' weakly better against all betting strategies
4. Show strict improvement against always-bet-s strategy

Key citation: Sierpinski (1922) for nonatomic measure subset existence.

### Monotone-Admissibility Discussion
Second monotonicity condition (call smaller bets more) not dominated but prevents exploitation:
- If caller violates, bettor takes smaller risks for higher returns
- Monotone-admissibility selects unique equilibrium

### Application to LCP
Bluff hand strength irrelevant against optimal caller, but matters against monotone deviations.
Unique monotone-admissible equilibrium: bluff larger with weaker hands.

## Figures
- TikZ diagram showing sets A, B and subsets A', B' for strategy improvement

## Dependencies
- Solving LCP section (references these definitions)
- Nash equilibrium proof (uses these lemmas)
