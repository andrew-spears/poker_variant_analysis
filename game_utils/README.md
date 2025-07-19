# game_utils - The Algorithmic Game Theory Library

A scalable and generalizable library for implementing and analyzing extensive-form games, with a focus on zero-sum games and equilibrium computation.

## Overview

This library provides a basic framework for:
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


## License

[Add your license information here]
