# Summary Analysis Section

## Purpose
High-level summary of parameter and payoff analysis for the main body. Detailed proofs in appendices.

## Key Content

### Payoff Visualization
References payoff heatmap figure showing how limits affect payoff distribution across hand combinations.

Key insight: Biggest wins/losses when both strong; extreme outcomes more pronounced but rarer with lenient limits.

### Expected Value Summary
References EV(x) figure and key observations:
- Bluffing hands: constant EV = x₂ - 1/2
- Checking hands: EV = x - 1/2
- Value betting: increasing returns, strongest hands bet largest

### Effect of Increasing U
Summarizes counterintuitive result:
- Most hands' EV decreases beyond some threshold U
- Explanation: caller adjusts conservatively across all bet sizes
- Only strongest hands (above v(U)) benefit from increased U

Bullet points of proven results:
- x₂ increases with U (more bluffing)
- Bet size v^(-1)(x) decreases with U for intermediate hands
- Calling cutoff c(v^(-1)(x)) increases despite smaller bets
- Threshold exists above which EV increases, below which it decreases

## Images
References images from payoff_analysis and parameter_analysis directories.

## Dependencies
- Appendix D (parameter_analysis proofs)
- Appendix E (payoff_analysis proofs)
