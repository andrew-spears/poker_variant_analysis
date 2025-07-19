# game_utils - The Algorithmic Game Theory Library

A scalable and generalizable library for implementing and analyzing extensive-form games, with a focus on zero-sum games and equilibrium computation.

## Overview

This library provides a comprehensive framework for:
- **Game Representation**: Abstract base classes for extensive-form games
- **Strategy Management**: Pure and mixed strategy implementations
- **Equilibrium Computation**: CFR (Counterfactual Regret Minimization) and linear programming solvers
- **Continuous Games**: Specialized implementations for continuous poker variants
- **Analysis Tools**: Visualization and utility functions for game analysis

## Core Components

### 1. Game Framework (`ZeroSumGame.py`)

The abstract base class for all zero-sum games:

```python
from game_utils.ZeroSumGame import ZeroSumGame

class MyGame(ZeroSumGame):
    # Implement required abstract methods:
    # - type_combos(): Return possible player type combinations
    # - all_info_sets(player): Return information sets for a player
    # - get_actions_at_info_set(info_set): Return available actions
    # - current_player(): Return current player index
    # - current_info_set(): Return current information set
    # - is_terminal(): Check if game is over
    # - _do_get_p1_payoff(): Return payoff for player 1
```

**Key Features:**
- Automatic normal-form conversion
- Expected payoff computation (exact and approximate)
- Pure strategy enumeration
- Random game state generation

### 2. Strategy Management (`Strategy.py`)

**PureStrategy**: Deterministic action selection at each information set
**MixedStrategy**: Probabilistic action selection with sampling capabilities

```python
from game_utils.Strategy import PureStrategy, MixedStrategy

# Create mixed strategy from normal form frequencies
mixed_strat = MixedStrategy.from_normal_form(frequencies, player, game)

# Sample actions from mixed strategy
action = mixed_strat.sample(info_set)
```

### 3. Equilibrium Solvers

#### CFR Solver (`CFR.py`)
Counterfactual Regret Minimization for approximate Nash equilibrium computation:

```python
from game_utils.CFR import CFRSolver

solver = CFRSolver(GameClass)
solver.train(iterations=10000)
strategy = solver.get_strategy(player=0)
```

#### Linear Programming (`LP.py`)
Exact Nash equilibrium computation for normal-form games:

```python
from game_utils.LP import solve_normal_zero_sum

strategy, game_value = solve_normal_zero_sum(payoff_matrix, player=0)
```

### 4. Continuous Poker Variants

Specialized implementations for continuous poker games:

- **LCP.py**: Limit Continuous Poker
- **NLCP.py**: No-Limit Continuous Poker  
- **FBCP.py**: Fixed Bet Continuous Poker
- **ContinuousPokerTemplate.py**: Base class for continuous poker variants

Each variant implements:
- Bet sizing functions
- Call thresholds
- Expected payoff computation
- Strategy visualization

### 5. Utility Functions (`utils.py`)

**Numerical Integration:**
```python
from game_utils.utils import integrate, double_integral
```

**Visualization:**
```python
from game_utils.utils import heatmap, binaryStrategyHeatmap
```

**Strategy Analysis:**
```python
from game_utils.utils import normalize, binaryStrategyArr
```

## Example Games

### Kuhn Poker (`kuhn.py`)
Three-card poker game with perfect information sets.

### Rock-Paper-Scissors (`RPS.py`)
Simple normal-form game implementation.

### Progressive Kuhn (`progressiveKuhn.py`)
Multi-round Kuhn poker variant.

## Usage Examples

### Basic Game Implementation
```python
from game_utils.ZeroSumGame import ZeroSumGame
from game_utils.InfoSet import InfoSet

class SimpleGame(ZeroSumGame):
    @classmethod
    def type_combos(cls):
        return [(None, None, None)]  # Single type game
    
    @classmethod
    def all_info_sets(cls, player):
        return [InfoSet.empty()]  # Single info set
    
    def current_player(self):
        return len(self.history) % 2
    
    def is_terminal(self):
        return len(self.history) >= 2
    
    def _do_get_p1_payoff(self):
        # Implement payoff logic
        pass
```

### CFR Training
```python
from game_utils.CFR import CFRSolver

# Train CFR solver
solver = CFRSolver(MyGame)
solver.train(10000)

# Get learned strategies
p1_strategy = solver.get_strategy(0)
p2_strategy = solver.get_strategy(1)

# Visualize strategies
from game_utils.utils import binaryStrategyHeatmap
binaryStrategyHeatmap(p1_strategy, title="Player 1 Strategy")
```

### Continuous Game Analysis
```python
from game_utils.ContinuousPokerVariants import LCP

# Analyze limit continuous poker
expected_payoff = LCP.expected_payoff(grid_size=1001)
LCP.generate_strategy_plot(save_path="strategy.png")
```

## Key Features

### Scalability
- **Modular Design**: Each component is independent and reusable
- **Abstract Interfaces**: Easy to implement new game types
- **Efficient Algorithms**: Optimized CFR and LP implementations
- **Memory Efficient**: Lazy evaluation and streaming for large games

### Generalizability
- **Game-Agnostic**: Framework works for any extensive-form game
- **Player Types**: Support for games with multiple player types
- **Information Sets**: Flexible information set representation
- **Continuous Games**: Specialized support for continuous action spaces

### Analysis Capabilities
- **Equilibrium Computation**: Both exact (LP) and approximate (CFR) methods
- **Strategy Visualization**: Heatmaps and strategy profiles
- **Payoff Analysis**: Expected value computation and analysis
- **Numerical Integration**: Tools for continuous game analysis

## Dependencies

- **NumPy**: Numerical computations
- **Matplotlib**: Visualization
- **SciPy**: Linear programming optimization

## Installation

```bash
pip install numpy matplotlib scipy
```

## Contributing

The library is designed for extensibility. To add a new game:

1. Inherit from `ZeroSumGame`
2. Implement required abstract methods
3. Add any game-specific analysis tools
4. Consider adding visualization functions

## Research Applications

This library has been used for:
- Poker game analysis and strategy computation
- Continuous game equilibrium analysis
- Algorithmic game theory research
- Educational demonstrations of game theory concepts

## License

[Add your license information here]
