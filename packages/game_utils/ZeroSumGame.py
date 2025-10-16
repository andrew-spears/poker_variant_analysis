from abc import ABC, abstractmethod
from typing import List
import numpy as np
from itertools import product
from game_utils.InfoSet import InfoSet
from game_utils.Strategy import PureStrategy, MixedStrategy

class ZeroSumGame(ABC):
    def __init__(self, p1_type, p2_type, nature_type, history):
        self.p1_type = p1_type
        self.p2_type = p2_type
        self.nature_type = nature_type
        self.history = history

    @classmethod
    def random(cls):
        """Return a game state with a random initial state, chosen from all combos of types."""
        type_combos = cls.type_combos()
        p1_type, p2_type, nature_type = type_combos[np.random.choice(len(type_combos))]
        return cls(p1_type=p1_type, p2_type=p2_type, nature_type=nature_type, history="")
    
    @classmethod
    def pure_strategies(cls, player):
        """Return a list of possible strategies for a given player."""
        info_sets = cls.all_info_sets(player)
        possible_actions_at_info_sets = []
        for i, I in enumerate(info_sets):
            actions = cls.get_actions_at_info_set(I)
            possible_actions_at_info_sets.append(actions)
        strategy_actions = list(product(*possible_actions_at_info_sets))
        
        strategies = []
        for actions in strategy_actions:
            strat = PureStrategy({I: actions[i] for i, I in enumerate(info_sets)}, cls)
            strategies.append(strat)
        return strategies
    
    @classmethod
    def expected_payoff_exact(cls, strategy1: PureStrategy, strategy2: PureStrategy):
        """
        TODO: accommodate for nature's type and randomness.
        """
        total_payoff = 0
        possible_types = cls.type_combos()
        for p1, p2, nature in possible_types:
            state = cls(p1_type=p1, p2_type=p2, nature_type=nature, history="")
            while not state.is_terminal():
                info_set = state.current_info_set()
                if state.current_player() == 0:
                    action = strategy1[info_set]
                else:
                    action = strategy2[info_set]
                state = state.get_next_state(action)
            total_payoff += state.get_payoff(0)
        return total_payoff / len(possible_types)
    
    @classmethod
    def expected_payoff_approx(cls, strategy1: MixedStrategy, strategy2: MixedStrategy, simulations=1000):
        """
        Approximates the expected payoff for player 0 by simulating many random playthroughs.
        Args:
            
        Returns:
            float: The average payoff for player 0 over many random playthroughs.
        """
        total_payoff = 0
        for _ in range(simulations):
            state = cls.random()
            while not state.is_terminal():
                info_set = state.current_info_set()
                if state.current_player() == 0:
                    action = strategy1.sample(info_set)
                else:
                    action = strategy2.sample(info_set)
                state = state.get_next_state(action)
            total_payoff += state.get_payoff(0)
        return total_payoff / simulations
    
    @classmethod
    def convert_to_normal(cls):
        """
        Approximate the normal-form representation of the extensive-form game
        by simulating many random playthroughs and recording payoffs.
        Assumes a two-player zero-sum game.
        return: 
            - payoff_matrix: a matrix where the rows correspond to strategies for player 1 and the columns correspond to strategies for player 2.
        Strategies are represented as PureStrategy objects.
        """
        # create a matrix indexed in rows by strategies for p1, columns for p2
        # each cell is the expected payoff for p1
        p1_strats = cls.pure_strategies(0)
        p2_strats = cls.pure_strategies(1)

        payoff_matrix = np.zeros((len(p1_strats), len(p2_strats)))
        for i, p1 in enumerate(p1_strats):
            for j, p2 in enumerate(p2_strats):
                payoff_matrix[i, j] = cls.expected_payoff_exact(p1, p2)
        return payoff_matrix
    
    def get_player_type(self, player: int) -> int:
        """Return the type of the given player. Return None if there is only one type."""
        if player == 0:
            return self.p1_type
        if player == 1:
            return self.p2_type
        raise ValueError("Invalid player index")

    def get_actions(self) -> List[str]:
        """Return available actions at this game state/info set. Return [] if game is over.
        Do not implement in subclass. Instead, implement _get_actions_at_info_set."""
        if self.is_terminal():
            return []
        info_set = self.current_info_set()
        return self.get_actions_at_info_set(info_set)
    
    def copy(self) -> 'AbstractGameState':
        """Return a copy of the game state. Assume the game state initialize takes p1_type, p2_type, history."""
        return self.__class__(p1_type=self.p1_type, p2_type=self.p2_type, nature_type=self.nature_type, history=self.history)
    
    def get_next_state(self, action: str) -> 'AbstractGameState':
        """Return a copy of the game state with updated history. Raise error if action is illegal or game is over."""
        if not action in self.get_actions():
            raise ValueError(f"Illegal action {action}")
        if self.is_terminal():
            raise ValueError("Game has already ended.")
        new_state = self.copy()
        new_state.history += action
        
        while new_state.current_player() == 2:
            # nature's turn
            if new_state.is_terminal():
                break
            new_state.history += self.get_nature_action()
        return new_state
    
    def get_nature_action(self) -> str:
        """Return the nature action for the current state. By default, raise an Error."""
        raise NotImplementedError("Nature action not implemented.")

    def get_payoff(self, player: int) -> int:
        """Return the payoff for a given player at a terminal state. Raise error if game is not over.
        Do not implement in subclass. Instead, implement _do_get_payoff."""
        assert self.is_terminal()
        if player == 0:
            return self._do_get_p1_payoff()
        else:
            return -self._do_get_p1_payoff()
        
    def __str__(self) -> str:
        """Return a string representation of the game state."""
        return f"{self.__class__.__name__}, P1 type: {self.p1_type}, P2 type: {self.p2_type}, Nature type: {self.nature_type}, History: {self.history}"
    
    def __repr__(self) -> str:
        """Return a formal string representation of the game state."""
        return self.__str__()
    
    @classmethod
    @abstractmethod
    def type_combos(cls):
        """Return a list of tuples of possible player-player-nature type combinations. Return [(None, None, None)] for games with only one type."""
        pass

    @classmethod
    @abstractmethod
    def all_info_sets(cls, player):
        """Return a list of possible information sets for a given player. Return [InfoSet.empty()] for games with only one info set."""
        pass
    
    @classmethod
    @abstractmethod
    def get_actions_at_info_set(self, info_set: 'InfoSet') -> List[str]:
        """Return available actions at this info set. Do not check if game is over."""
        pass

    @abstractmethod
    def current_player(self) -> int:
        """Return the index of the current player, or 2 for nature. May return anything if the game is over."""
        pass
    
    @abstractmethod
    def current_info_set(self):
        """Return the information set for the current player as an InfoSet. In a single-info set game, return InfoSet.empty()."""
        pass
    
    @abstractmethod
    def is_terminal(self) -> bool:
        """Return whether the game has reached a terminal state."""
        pass

    @abstractmethod
    def _do_get_p1_payoff(self) -> int:
        """Return the payoff for the maximizing player at a terminal state. Do not check if game is over."""
        pass

    

    