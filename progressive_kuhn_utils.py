import numpy as np
import random

FourCardHands = np.array(range(4))
FourCardHandsSet = set(range(4))

class Distribution:
    def __init__(self, probs):
        self.probs = np.array(probs, dtype=float)
        self.probs /= np.sum(self.probs)

class FourCardState:
    def __init__(self, bettor_hand, caller_hand, revealed_card, history=None):
        self.bettor_hand = bettor_hand
        self.caller_hand = caller_hand
        self.revealed_card = revealed_card
        if history is None:
            history = []
        self.history = history
        self.folded = False
        self.over = False

    def street(self):
        return len(self.history)

    def __str__(self):
        if self.over:
            return f"B{self.bettor_hand}, C{self.caller_hand}, {self.history}, Payoff: {self.get_payoff()}"
        return f"B{self.bettor_hand}, C{self.caller_hand}, {self.history}, Pot: {self.pot()}"

    def __repr__(self):
        return self.__str__()
    
    def bettor_possibilities(self):
        if self.street() == 0:
            return FourCardHandsSet - {self.caller_hand}
        elif self.street() == 1:
            # any card other than the caller and the revealed card
            return FourCardHandsSet - {self.caller_hand, self.revealed_card}
        else:
            raise ValueError("Game over")
        
    def caller_possibilities(self):
        if self.street() == 0:
            return FourCardHandsSet - {self.bettor_hand}
        elif self.street() == 1:
            # any card other than the bettor and the revealed card
            return FourCardHandsSet - {self.bettor_hand, self.revealed_card}
        else:
            raise ValueError("Game over")

    def apply_actions(self, bettor_action, caller_action):
        self.history.append(max(bettor_action, caller_action))
        if bettor_action == 1 and caller_action == 0: # fold
            self.fold()
            return
            
        if self.street() == 2: # check or call to showdown
            self.showdown()

    def pot(self):
        return 2 + 2* sum(self.history)

    def fold(self):
        self.folded = True
        self.over = True
        print("Folded")

    def showdown(self):
        self.over=True
        print("Showdown")

    def get_payoff(self):
        if self.folded:
            return self.pot()//2
        elif self.over:
            if self.bettor_hand > self.caller_hand:
                return self.pot()//2
            else:
                return -self.pot()//2
        else:
            return 0 # still going

class FourCardStrategy:
    def __init__(self, s0actions, s1actions):
        self.s0actions = np.array(s0actions)
        self.s1actions = np.array(s1actions)

    def get_freq(self, state, hand):
        if state.street() == 0:
            return self.s0actions[hand]
        elif state.street() == 1:
            # index into our array by history, revealed card, hand
            return self.s1actions[state.history[-1]][state.revealed_card][hand] 
        else:
            raise ValueError("Game over")

    def get_action(self, state, hand):
        freq = self.get_freq(state, hand)
        return 1 if np.random.random() < freq else 0

class FourCardBettor(FourCardStrategy):
    def get_action(self, state):
        return super().get_action(state, state.bettor_hand)
    
class FourCardCaller(FourCardStrategy):
    def get_action(self, state):
        return super().get_action(state, state.caller_hand)
    
    def get_bet_ev_against(self, state: FourCardState, caller_distr: Distribution):
        '''
        Returns the expected value FOR THE BETTOR of betting against a caller with the given distribution.
        '''
        if state.street() == 0:
            raise NotImplementedError("Not implemented for street 0")
        elif state.street() == 1:
            fold_probs = np.array([1-self.get_freq(state, hand) for hand in FourCardHands])
            fold_prob = np.dot(fold_probs, caller_distr.probs)
            call_probs = np.array([self.get_freq(state, hand) for hand in FourCardHands])
            call_win_probs = np.where(FourCardHands < state.bettor_hand, call_probs, np.zeros_like(call_probs))
            call_lose_probs = np.where(FourCardHands > state.bettor_hand, call_probs, np.zeros_like(call_probs))
            call_win_prob = np.dot(call_win_probs, caller_distr.probs)
            call_lose_prob = np.dot(call_lose_probs, caller_distr.probs)
            ev = (state.pot()//2 + 1) * (call_win_prob - call_lose_prob)  + (state.pot()//2) *fold_prob
            return ev
        else:
            raise ValueError("Game over")
        
    def get_check_ev_against(self, state: FourCardState, caller_distr: Distribution):
        '''
        Returns the expected value FOR THE BETTOR of checking against a caller with the given distribution.
        '''
        if state.street() == 0:
            raise NotImplementedError("Not implemented for street 0")
        elif state.street() == 1:
            wins = np.where(FourCardHands < state.bettor_hand, np.ones_like(FourCardHands), np.zeros_like(FourCardHands))
            losses = np.where(FourCardHands > state.bettor_hand, np.ones_like(FourCardHands), np.zeros_like(FourCardHands))
            win_prob = np.dot(wins, caller_distr.probs)
            loss_prob = np.dot(losses, caller_distr.probs)
            ev = (win_prob - loss_prob) * (state.pot()//2)
            return ev
        else:
            raise ValueError("Game over")
        
def FourCardRunout(bettor: FourCardBettor, caller: FourCardCaller, bettor_hand=None, caller_hand=None, revealed_card=None):
    remaining = list(FourCardHandsSet - {revealed_card, bettor_hand, caller_hand})
    random.shuffle(remaining)
    if bettor_hand is None:
        bettor_hand = remaining.pop()
    if caller_hand is None:
        caller_hand = remaining.pop()
    if revealed_card is None:
        revealed_card = remaining.pop()

    state = FourCardState(bettor_hand, caller_hand, revealed_card)
    print(state)
    while not state.over:
        bettor_action = bettor.get_action(state)
        caller_action = caller.get_action(state)
        state.apply_actions(bettor_action, caller_action)
        print(state)
    return state.get_payoff()