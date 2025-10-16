# Notebooks

This directory contains Jupyter notebooks for analysis, visualization, and experimentation with poker game theory.

## Limit Continuous Poker

**Location:** [limit_continuous_poker/](limit_continuous_poker/)

Numerical analysis and visualizations for the Limit Continuous Poker paper:

- **[visualizations.ipynb](limit_continuous_poker/visualizations.ipynb)** - Main visualizations for the paper (strategy profiles, payoff heatmaps, game value plots)
- **[numerical_analysis.ipynb](limit_continuous_poker/numerical_analysis.ipynb)** - Numerical simulations and verification of analytical results
- **[solve_sympy_final.ipynb](limit_continuous_poker/solve_sympy_final.ipynb)** - Symbolic solutions using SymPy
- **[solve_wolfram.ipynb](limit_continuous_poker/solve_wolfram.ipynb)** - Solutions via Wolfram Mathematica

**Paper:** [../papers/limit_continuous_poker/](../papers/limit_continuous_poker/)

## Classic Poker Variants

Analysis of well-known simplified poker models:

- **[kuhnAnalysis.ipynb](kuhnAnalysis.ipynb)** - Kuhn poker analysis and CFR solving
- **[progressiveKuhnAnalysis.ipynb](progressiveKuhnAnalysis.ipynb)** - Progressive Kuhn poker variant
- **[vonneumann.ipynb](vonneumann.ipynb)** - Von Neumann (Fixed-Bet Continuous) poker

## Other Analyses

- **[RPS.ipynb](RPS.ipynb)** - Rock-Paper-Scissors as a simple game theory example
- **[headsup_pushfold.ipynb](headsup_pushfold.ipynb)** - Heads-up push/fold analysis
- **[four_card_progressive_kuhn_analysis.ipynb](four_card_progressive_kuhn_analysis.ipynb)** - 4-card Progressive Kuhn variant

## Running the Notebooks

1. **Install dependencies:**
   ```bash
   cd .. # to repo root
   pip install -e .
   pip install jupyter notebook
   ```

2. **Launch Jupyter:**
   ```bash
   jupyter notebook
   ```

3. **Open any notebook** and run the cells

All notebooks import from the `game_utils` package located in [../packages/game_utils/](../packages/game_utils/).
