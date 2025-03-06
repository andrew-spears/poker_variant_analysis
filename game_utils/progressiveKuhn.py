# import numpy as np
# from game_utils.ZeroSumGame import ZeroSumGame
# from game_utils.InfoSet import InfoSet
# from abc import ABC, abstractmethod


# class ProgressiveKuhn(ZeroSumGame, ABC):
#     def __init__(self, p1_type, p2_type, history):
#         n = self.__class__.n
#         assert n > p1_type and n > p2_type and p1_type >= 0 and p2_type >= 0
#         self.n = n
#         super().__init__(p1_type, p2_type, history)

#     @classmethod
#     def nCard(cls, n_cards):
#         '''
#         Returns a subclass of KuhnState with n_cards as the number of cards in the deck.
#         '''
#         class subclass(ProgressiveKuhn):
#             n = n_cards
#             def __init__(self, p1_type, p2_type, history):
#                 super().__init__(p1_type, p2_type, history)

#             def __str__(self):
#                 return f"Kuhn({self.n}), P1 type: {self.p1_type}, P2 type: {self.p2_type}, History: {self.history}"
#         return subclass

#     @classmethod
#     def random(cls):
#         """ Create a random Kuhn poker state """
#         n = cls.n
#         deck = list(range(n))
#         np.random.shuffle(deck)
#         return cls(deck.pop(), deck.pop(), "")
    
#     @classmethod
#     def types(cls):
#         # p1, p2 must have distinct cards
#         combos = []
#         for i in range(cls.n):
#             for j in range(cls.n):
#                 if i == j:
#                     continue
#                 combos.append((i, j))
#         return combos
        
#     def get_current_player(self):
#         """ Return the current player (0 = P1, 1 = P2) """
#         return len(self.history) % 2

#     def get_info_set(self):
#         # each player can see the whole history
#         player = self.get_current_player()
#         card = self.p1_type if player == 0 else self.p2_type
#         assert self.history is not None
#         return InfoSet(card, self.history)

#     @classmethod
#     def get_actions_at_info_set(self, info_set):
#         if info_set.history == "":
#             return ["K", "B"]
#         return ["F", "C"] if info_set.history[-1] == "B" else ["K", "B"]

#     @classmethod
#     def info_sets(cls, player):
#         # each player can see the whole history
#         info_sets = []
#         if player == 0:
#             histories = ["", "KB"]
#         elif player == 1:
#             histories = ["K", "B"]
#         for card in range(cls.n):
#             for h in histories:
#                 info_sets.append(InfoSet(card, h))
#         return info_sets

#     def is_terminal(self):
#         return self.history in ['BC', 'KK', 'BF', 'KBC', 'KBF']
    
#     def get_pot(self):
#         """ Return the current pot size, including the ante """
#         if self.history in ['BC', 'KBC']:
#             return 4
#         else:
#             return 2

#     def _do_get_p1_payoff(self):
#         if self.history[-1] == "F":
#             p1_payoff = self.get_pot()//2 if self.get_current_player() == 0 else -self.get_pot()//2
#         else:
#             p1_payoff = self.get_pot()//2 if self.p1_type > self.p2_type else -self.get_pot()//2
#         return p1_payoff
    
# class KuhnNoCheck(Kuhn):
#     # Kuhn poker, but if player 1 checks, we go straight to showdown
#     @classmethod
#     def nCard(cls, n_cards):
#         '''
#         Returns a subclass with n_cards as the number of cards in the deck.
#         '''
#         class subclass(KuhnNoCheck):
#             n = n_cards
#             def __init__(self, p1_type, p2_type, history):
#                 super().__init__(p1_type, p2_type, history)

#             def __str__(self):
#                 return f"KuhnNoCheck({self.n}), P1 type: {self.p1_type}, P2 type: {self.p2_type}, History: {self.history}"
#         return subclass

#     @classmethod
#     def info_sets(cls, player):
#         # each player can see the whole history
#         info_sets = []
#         if player == 0:
#             histories = [""]
#         elif player == 1:
#             histories = ["B"]
#         for card in range(cls.n):
#             for h in histories:
#                 info_sets.append(InfoSet(card, h))
#         return info_sets

#     def is_terminal(self):
#         return self.history in ['BC', 'K', 'BF']
    
# ThreeCard = Kuhn.nCard(3)
# ThreeCardNoCheck = KuhnNoCheck.nCard(3)