import numpy as np
from game_utils.kuhn import Kuhn
from game_utils.InfoSet import InfoSet
from game_utils import utils
from abc import ABC, abstractmethod
from itertools import permutations, product

class ProgressiveKuhn(Kuhn, ABC):
    def __init__(self, p1_type, p2_type, nature_type, history, **kwargs):
        n = self.__class__.n
        assert n > p1_type and n > p2_type and p1_type >= 0 and p2_type >= 0
        self.n = n
        super().__init__(p1_type=p1_type, p2_type=p2_type, nature_type=nature_type, history=history)

    @classmethod
    def hist_since_nature_action(cls, history):
        '''
        return the history since the last reveal
        '''
        nature_actions_inds = [i for i, c in enumerate(history) if c.isnumeric()]
        if len(nature_actions_inds) == 0: 
            return history
        return history[nature_actions_inds[-1]+1:]

    @classmethod
    def type_combos(self):
        # p1, p2 must have distinct cards, and nature will reveal the remaining cards in some order
        combos = []
        # get all permutations of n cards
        perms = list(permutations(range(self.n)))
        for p in perms:
            combos.append((p[0], p[1], "".join([str(x) for x in p[2:]])))
        return combos
    
    @classmethod
    def all_info_sets(cls, player):
        # betting_round_histories = ["KK", "KBC", "BC"]
        betting_round_histories = ["K", "BC"]
        if player == 0:
            partial_betting_round_histories = [""]
        if player == 1:
            partial_betting_round_histories = ["B"]
            # partial_betting_round_histories = ["K", "B"]

        info_sets = []
        for hand in range(cls.n):
            # there can be at most n-3 reveals.
            # each can have a full betting round before
            # then a partial betting round at the end
            for num_reveals in range(cls.n-2):
                # interleave possible betting round histories with the reveals
                # this gives the history up until the final partial betting round
                possible_reveals = [str(x) for x in range(cls.n) if x != hand]
                interleavings = utils.generate_interleavings(betting_round_histories, True, num_reveals, possible_reveals, False, num_reveals)

                # now find combinations of interleavings with partial betting round histories at the end.
                full_histories = utils.generate_interleavings(interleavings, False, 1, partial_betting_round_histories, False, 1)
                for history in full_histories:
                    info_sets.append(InfoSet(hand, history))
        return info_sets
    
    @classmethod
    def get_actions_at_info_set(cls, info_set):
        # find last nature action (numbers)
        hist = cls.hist_since_nature_action(info_set.history)
        if hist == "":
            return ["K", "B"]

        if hist in ["B"]:
            return ["F", "C"]
        raise ValueError(f"Invalid info set: {info_set}")

    def get_nature_action(self):
        '''
        reveal a card from the deck. Nature's type dictates the order in which to reveal cards
        '''
        past_nature_actions = len([i for i, c in enumerate(self.history) if c.isnumeric()])
        return str(self.nature_type[past_nature_actions])

    def current_player(self) -> int:
        """Return the index of the current player, or 2 for nature. May return anything if the game is over."""
        # find last nature action (numbers)
        hist = self.hist_since_nature_action(self.history)

        if hist in ["", "KB"]:
            return 0
        # if hist in ["K", "B"]:
        if hist in ["B"]:
            return 1
        # if hist in ["KK", "BC", "KBC"]: # natures turn
        if hist in ["K", "BC"]: # natures turn
            return 2
    
    def is_terminal(self) -> bool:
        """Return whether the game has reached a terminal state."""
        if len(self.history) > 0:
            if self.history[-1] == "F":
                return True # folded
        # play ends when nature has one card unrevealed and the betting round is over
        past_nature_actions = len([i for i, c in enumerate(self.history) if c.isnumeric()])
        total_unrevealed = len(self.nature_type) - past_nature_actions
        return total_unrevealed == 1 and self.current_player() == 2

   
