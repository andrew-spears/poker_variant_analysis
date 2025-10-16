import numpy as np
from game_utils.ZeroSumGame import ZeroSumGame
from game_utils.InfoSet import InfoSet
from abc import ABC, abstractmethod


class Kuhn(ZeroSumGame, ABC):
    def __init__(self, p1_type, p2_type, history, **kwargs):
        n = self.__class__.n
        assert n > p1_type and n > p2_type and p1_type >= 0 and p2_type >= 0
        super().__init__(p1_type=p1_type, p2_type=p2_type, nature_type=kwargs.get('nature_type', None), history=history)

    @classmethod
    def nCard(cls, n_cards):
        '''
        Returns a subclass of KuhnState with n_cards as the number of cards in the deck.
        '''
        class ncardSubclass(cls):
            n = n_cards
        # print(cls)
        # print(ncardSubclass)
        ncardSubclass.__name__ =  f"{cls.__name__}({n_cards})"
        return ncardSubclass

    @classmethod
    def type_combos(cls):
        # p1, p2 must have distinct cards
        combos = []
        for i in range(cls.n):
            for j in range(cls.n):
                if i == j:
                    continue
                combos.append((i, j, None))
        return combos
        
    def current_player(self):
        """ Return the current player (0 = P1, 1 = P2) """
        return len(self.history) % 2

    def current_info_set(self):
        # each player can see the whole history
        player = self.current_player()
        assert player in (0, 1) # should never be finding info set for nature
        card = self.p1_type if player == 0 else self.p2_type
        assert self.history is not None
        return InfoSet(card, self.history)

    @classmethod
    def get_actions_at_info_set(cls, info_set):
        if info_set.history == "":
            return ["K", "B"]
        return ["F", "C"] if info_set.history[-1] == "B" else ["K", "B"]

    @classmethod
    def all_info_sets(cls, player):
        # each player can see the whole history
        info_sets = []
        if player == 0:
            histories = ["", "KB"]
        elif player == 1:
            histories = ["K", "B"]
        for card in range(cls.n):
            for h in histories:
                info_sets.append(InfoSet(card, h))
        return info_sets

    def is_terminal(self):
        return self.history in ['BC', 'KK', 'BF', 'KBC', 'KBF']
    
    def get_pot(self):
        """ Return the current pot size, including the ante """
        # for each call (and implicit bet), the pot increases by 2
        # pot starts at 2
        calls = self.history.count("C")
        return 2 + 2 * calls

    def _do_get_p1_payoff(self):
        if self.history[-1] == "F": # last player to act folded
            previous_state = self.copy()
            previous_state.history = previous_state.history[:-1]
            folder = previous_state.current_player()
            p1_payoff = self.get_pot()//2 if folder == 1 else -self.get_pot()//2
        else:
            p1_payoff = self.get_pot()//2 if self.p1_type > self.p2_type else -self.get_pot()//2
        return p1_payoff
    
class HalfStreetKuhn(Kuhn):
    # Kuhn poker, but if player 1 checks, we go straight to showdown

    @classmethod
    def all_info_sets(cls, player):
        # each player can see the whole history
        info_sets = []
        if player == 0:
            histories = [""]
        elif player == 1:
            histories = ["B"]
        for card in range(cls.n):
            for h in histories:
                info_sets.append(InfoSet(card, h))
        return info_sets

    def is_terminal(self):
        return self.history in ['BC', 'K', 'BF']
    
ThreeCard = Kuhn.nCard(3)
ThreeCardHalfStreet = HalfStreetKuhn.nCard(3)