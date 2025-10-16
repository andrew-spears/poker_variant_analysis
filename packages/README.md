# Packages

This directory contains reusable Python packages for game theory and poker analysis.

## game_utils

A game theory toolkit for implementing and analyzing extensive-form games, with a focus on poker variants.

**Key Features:**
- Abstract framework for zero-sum games
- Nash equilibrium solvers (CFR, Linear Programming)
- Implementations of classic poker variants (Kuhn, Progressive Kuhn, RPS)
- Continuous poker variants (LCP, NLCP, FBCP)
- Visualization and analysis utilities

**Documentation:** See [game_utils/README.md](game_utils/README.md) for detailed API documentation and usage examples.

**Installation:**

From the root of the repository:
```bash
pip install -e .
```

Then import in your Python code:
```python
from game_utils.ContinuousPokerVariants.LCP import LCP
from game_utils.CFR import CFRSolver
from game_utils.kuhn import Kuhn
```

## Dependencies

- numpy >= 1.20
- scipy >= 1.7
- matplotlib >= 3.4
- sympy >= 1.9
- Python >= 3.8
