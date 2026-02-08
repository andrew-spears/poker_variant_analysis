# Introduction Section

## Purpose
Introduces Limit Continuous Poker (LCP) and establishes its context within game theory and poker research.

## Key Content

### Background
- Simplified poker models isolate strategic aspects (bluffing, value betting, bet sizing) while remaining tractable
- Historical context: von Neumann/Morgenstern (1944), Kuhn poker, computational solutions to Texas hold'em

### Two Classical Variants Reviewed

**Fixed-Bet Continuous Poker (FBCP):**
- Players each ante 0.5, dealt hand strengths from [0,1]
- Bettor checks or bets fixed amount B; caller calls or folds
- Unique admissible Nash equilibrium: bluff weak hands, value bet strong hands, check middle
- Value maximized at pot-sized bet (B=1)

**No-Limit Continuous Poker (NLCP):**
- Bettor can choose any bet size s > 0
- Pure strategies: weakest hands bluff large, strongest hands value bet large
- Value = 1/14 (for 0.5 ante)

### LCP Contributions
1. **Nash Equilibrium Solution**: Closed-form expressions with six thresholds and two bet-sizing functions
2. **Game Value Analysis**: Rational formula with symmetry V(L,U) = V(1/U, 1/L)
3. **Convergence Results**: LCP → FBCP and NLCP at appropriate limits
4. **Parameter Sensitivity**: Counterintuitive effects where expanding options can reduce EV

## Images
- `images/NLCP_strategy_profile.png` - NLCP strategy visualization

## Key References
- Ferguson and Ferguson (FBCP analysis)
- Chen and Ankenman (NLCP/"Mathematics of Poker")
- Sion's minimax theorem (game value existence)
