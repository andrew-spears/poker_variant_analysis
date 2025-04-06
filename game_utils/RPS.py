from abc import ABC, abstractmethod
from game_utils.ZeroSumGame import ZeroSumGame
from game_utils.InfoSet import InfoSet
from typing import List
import numpy as np

class RPS(ZeroSumGame):
    ACTIONS = ["R", "P", "S"]
    # zero sum, write payoff for player 1
    PAYOFF_MATRIX = {
        ("R", "R"): 0,
        ("R", "P"): -1,
        ("R", "S"): 1,
        ("P", "R"): 1,
        ("P", "P"): 0,
        ("P", "S"): -1,
        ("S", "R"): -1,
        ("S", "P"): 1,
        ("S", "S"): 0,
    }
    
    def __init__(self, history=None, **kwargs):
        if history is None:
            history = ""
        super().__init__(None, None, history)

    def copy(self):
        return RPS(self.history)
    
    def current_player(self) -> int:
        return len(self.history) % 2
    
    def current_info_set(self):
        return InfoSet(None, None)
    
    @classmethod
    def get_actions_at_info_set(cls, info_set) -> List[str]:
        return cls.ACTIONS

    def is_terminal(self) -> bool:
        return len(self.history) == 2
    
    @classmethod
    def random(cls):
        return RPS("")
    
    def _do_get_p1_payoff(self) -> int:
        return self.PAYOFF_MATRIX[(self.history[0], self.history[1])]
    
    @classmethod
    def type_combos(cls):
        return [(None, None)]  # No inherent types, just two players

    @classmethod
    def all_info_sets(cls, player):
        return [InfoSet(None, None)]  # No info sets, just two players