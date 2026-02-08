from typing import Dict, Any, Callable, Tuple
import numpy as np
from game_utils2.core.game import SequentialGame


class Strategy:
    def __init__(
        self,
        game: SequentialGame,
        strategy: Callable[[Tuple[Any, ...], Any], Dict[Any, float]],
    ):
        self.game = game
        self.strategy = strategy  # history x type -> {actions : probabilities}

    def get_freqs(self, history, type):
        freqs = self.strategy(history, type)
        legal_actions = self.game.get_actions(history)
        for action in freqs.keys():
            assert action in legal_actions, "strategy gives illegal actions"
        assert np.isclose(sum(freqs.values()), 1), f"strategy must return a probability distribution over actions, instead got {freqs}"
        return freqs

    def sample_action(self, history, type, seed=None):
        np.random.seed(seed)
        freqs = self.get_freqs(history, type)
        actions = list(freqs.keys())
        probabilities = list(freqs.values())
        return np.random.choice(actions, p=probabilities)


class StrategyProfile:
    def __init__(
        self, game: SequentialGame, p0_strategy: Strategy, p1_strategy: Strategy
    ):
        self.game = game
        self.p0_strategy = p0_strategy
        self.p1_strategy = p1_strategy
        assert p0_strategy.game == game, "Strategy's game must match the game of the profile"
        assert p1_strategy.game == game, "Strategy's game must match the game of the profile"

    def sample_outcome(self, seed=None):
        # return types, history, payoff
        np.random.seed(seed)
        inst = self.game.get_instance()
        types = inst.types
        while not inst.is_terminal():
            p0_action = self.p0_strategy.sample_action(inst.history, types[0], seed=seed)
            inst.play_action(p0_action, inplace=True)
            if inst.is_terminal():
                break
            p1_action = self.p1_strategy.sample_action(inst.history, types[1], seed=seed)
            inst.play_action(p1_action, inplace=True)
        payoff = inst.get_payoff()
        return types, inst.history, payoff