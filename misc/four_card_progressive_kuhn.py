import numpy as np
import random
from game_utils.utils import cond_print

FourCardHands = np.array(range(4))
FourCardHandsSet = set(range(4))

class Distribution:
    def __init__(self, keys, probs=None, function=None, normalize=False):
        if probs is None:
            if function is None:
                raise ValueError("Must provide either probs or function")
            probs = [function(key) for key in keys]
        self.keys = keys
        self.probs = np.array(probs, dtype=float)
        if normalize:
            self.probs /= np.sum(self.probs)

    def __str__(self):
        return f"Keys: {self.keys}, Probs: {self.probs}"
    
    def __repr__(self):
        return str(self)
    
    def __mul__(self, other):
        assert isinstance(other, Distribution)
        if len(other.keys) != len(self.keys):
            raise ValueError("Key lengths do not match")
        return Distribution(self.keys, self.probs * other.probs)
    
    def normalize(self):
        return Distribution(self.keys, self.probs, normalize=True)
    
    def sum(self):
        return np.sum(self.probs)

    def sum_where(self, boolean_function):
        return sum(np.where(boolean_function(self.keys), self.probs, 0))
    
    def dot(self, other):
        if len(other.keys) != len(self.keys):
            raise ValueError("Key lengths do not match")
        return np.dot(self.probs, other.probs)
    
    def event_prob(self, event_freqs):
        '''
        Returns the probability of an event occurring given the frequencies of the event for each key.
        '''
        return np.dot(self.probs, event_freqs)
    
    def update(self, event_freqs):
        '''
        Use bayes rule to update a distribution based on the frequencies of an event occurring for given keys.
        P[key|event] = P[key] * P[event|key] / P[event]
        '''
        assert len(event_freqs) == len(self.keys), "Event frequencies must have the same length as keys"
        event_prob = self.event_prob(event_freqs)
        if event_prob == 0: 
            # this event is impossible given the current distribution. return all 0s
            return Distribution(self.keys, [0]*len(self.keys))
        
        new_probs = self.probs * event_freqs / event_prob
        return Distribution(self.keys, new_probs)

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
        cards = ["-"]*4
        cards[self.bettor_hand] = "B"
        cards[self.caller_hand] = "C"
        if self.street() > 0:
            cards[self.revealed_card] = "R"
        if self.over:
            return f"{cards}, Pot: {self.pot()}, Payoff: {self.get_payoff()}" + (", Folded" if self.folded else "")
        return f"{cards}, Pot: {self.pot()}"

    def __repr__(self):
        return self.__str__()
    
    def bettor_possibilities(self, onehot=False):
        if self.street() == 0:
            out = FourCardHandsSet - {self.caller_hand}
        elif self.street() == 1:
            # any card other than the caller and the revealed card
            out = FourCardHandsSet - {self.caller_hand, self.revealed_card}
        else:
            raise ValueError("Game over")
        if onehot:
            return [1 if i in out else 0 for i in FourCardHands]
        return out
        
    def caller_possibilities(self, onehot=False):
        if self.street() == 0:
            out = FourCardHandsSet - {self.bettor_hand}
        elif self.street() == 1:
            # any card other than the bettor and the revealed card
            out = FourCardHandsSet - {self.bettor_hand, self.revealed_card}
        else:
            raise ValueError("Game over")
        if onehot:
            return [1 if i in out else 0 for i in FourCardHands]
        return out

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

    def get_bet_size(self):
        return 1

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
    
    def call_ev_against(self, state: FourCardState, bettor_distr: Distribution, verbose=False):
        '''
        Returns the expected value FOR THE CALLER of calling against a bettor with the given distribution.
        '''
        if state.street() == 0:
            # if we call, there are 3 possible revealed cards. 
            # We then have to consider the opponent calling or checking street 1. 
            # Find the ev in each case and take the average.
            possible_reveals = list(FourCardHandsSet - {state.caller_hand})
            future_evs = []
            cond_print(f"Evaluating Call ev in state {state}", verbose)
            for reveal in possible_reveals:
                new_state = FourCardState(state.bettor_hand, state.caller_hand, reveal, state.history + [1])
                cond_print(f"Evaluating state {new_state}", verbose)
                bet_freqs = [self.get_freq(new_state, hand) for hand in FourCardHands]
                
                # update our bettor distribution given the revealed card
                bettor_distr_given_reveal = bettor_distr.update([0 if hand == reveal else 1 for hand in FourCardHands])
                cond_print(f"Bettor distr: {bettor_distr_given_reveal}", verbose)

                # consider case where the bettor bets on the next street
                # update our distr, then max between calling and folding
                bettor_distr_given_bet = bettor_distr_given_reveal.update(bet_freqs)
                cond_print(f"Bettor distr given bet: {bettor_distr_given_bet}", verbose)
                future_ev_given_bet = max(self.call_ev_against(new_state, bettor_distr_given_bet), self.fold_ev_against(new_state, bettor_distr_given_bet))

                # consider case where the bettor checks on the next street
                bettor_distr_given_check = bettor_distr_given_reveal.update([1-self.get_freq(new_state, hand) for hand in FourCardHands])
                cond_print(f"Bettor distr given check: {bettor_distr_given_check}", verbose)
                win_prob = bettor_distr_given_check.sum_where(lambda hand : hand < state.caller_hand)
                lose_prob = bettor_distr_given_check.sum_where(lambda hand : hand > state.caller_hand)
                future_ev_given_check = (new_state.pot()//2) * (win_prob - lose_prob)

                # combine the two using probabilities of each case
                bet_prob_given_reveal = bettor_distr_given_reveal.event_prob(bet_freqs)
                cond_print(f"Bet probability: {bet_prob_given_reveal}", verbose)
                cond_print(f"EV given bet: {future_ev_given_bet}", verbose)
                check_prob_given_reveal = bettor_distr_given_reveal.event_prob([1-freq for freq in bet_freqs])
                cond_print(f"Check probability: {check_prob_given_reveal}", verbose)
                cond_print(f"EV given check: {future_ev_given_check}", verbose)

                future_ev = bet_prob_given_reveal * future_ev_given_bet + check_prob_given_reveal * future_ev_given_check
                cond_print(f"EV given revealed card {reveal}: {future_ev}", verbose)

                future_evs.append(future_ev)

            return np.mean(future_evs)
        elif state.street() == 1:
            # probability of having and betting with certain hands
            bet_distr = bettor_distr.update([self.get_freq(state, hand) for hand in FourCardHands])

            win_prob = bet_distr.sum_where(lambda hand : hand < state.caller_hand)
            lose_prob = bet_distr.sum_where(lambda hand : hand > state.caller_hand)

            ev = (state.pot()//2 + 1) * (win_prob - lose_prob)
            return ev
        else:
            raise ValueError("Game over")
        
    def fold_ev_against(self, state: FourCardState, bettor_distr: Distribution):
        '''
        Returns the expected value FOR THE CALLER of folding against a bettor with the given distribution.
        '''
        return -state.pot()//2
    
class FourCardCaller(FourCardStrategy):
    def get_action(self, state):
        return super().get_action(state, state.caller_hand)
    
    def bet_ev_against(self, state: FourCardState, caller_distr: Distribution, verbose=False):
        '''
        Returns the expected value FOR THE BETTOR of betting against a caller with the given distribution.
        '''
        if state.street() == 0:
            # if we bet, there are 2 cases: call or fold. 
            fold_distr = caller_distr.update([1-self.get_freq(state, hand) for hand in FourCardHands])
            fold_prob = fold_distr.sum()

            call_distr = caller_distr.update([self.get_freq(state, hand) for hand in FourCardHands])
            call_prob = call_distr.sum()

            # if called, there are 3 possible revealed cards. Find the ev in each case and take the average
            possible_reveals = list(FourCardHandsSet - {state.bettor_hand})
            future_evs = []
            cond_print(f"Evaluating Bet ev in state {state}", verbose)
            for reveal in possible_reveals:
                new_state = FourCardState(state.bettor_hand, state.caller_hand, reveal, state.history + [1])
                cond_print(f"Evaluating state {new_state}", verbose)
                bet_ev = self.bet_ev_against(new_state, caller_distr)
                check_ev = self.check_ev_against(new_state, caller_distr)
                future_ev = max(bet_ev, check_ev)
                cond_print(f"EV given revealed card {reveal}: {future_ev}", verbose)
                future_evs.append(future_ev)
            ev = call_prob * np.mean(future_evs) + fold_prob * (state.pot()//2)
            return ev
        elif state.street() == 1:
            # probability of having and folding with certain hands
            fold_distr = caller_distr.update([1-self.get_freq(state, hand) for hand in FourCardHands])
            fold_prob = fold_distr.sum()

            #  probability of having and calling with certain hands
            call_distr = caller_distr.update([self.get_freq(state, hand) for hand in FourCardHands])
            call_win_prob = call_distr.sum_where(lambda hand : hand < state.bettor_hand)
            call_lose_prob = call_distr.sum_where(lambda hand : hand > state.bettor_hand)

            ev = (state.pot()//2 + state.get_bet_size()) * (call_win_prob - call_lose_prob)  + (state.pot()//2) *fold_prob
            return ev
        else:
            raise ValueError("Game over")
        
    def check_ev_against(self, state: FourCardState, caller_distr: Distribution, verbose=False):
        '''
        Returns the expected value FOR THE BETTOR of checking against a caller with the given distribution.
        '''
        if state.street() == 0:
            # if we check, there are 3 possible revealed cards. Find the ev in each case and take the average.
            possible_reveals = list(FourCardHandsSet - {state.bettor_hand})
            future_evs = []
            cond_print(f"Evaluating Check ev in state {state}", verbose)
            for reveal in possible_reveals:
                new_state = FourCardState(state.bettor_hand, state.caller_hand, reveal, state.history + [0])
                cond_print(f"Evaluating state {new_state}", verbose)
                future_bet_ev = self.bet_ev_against(new_state, caller_distr)
                future_check_ev = self.check_ev_against(new_state, caller_distr)
                future_ev = max(future_bet_ev, future_check_ev)
                cond_print(f"EV given revealed card {reveal}: {future_ev}", verbose)
                future_evs.append(future_ev)
            return np.mean(future_evs)
        elif state.street() == 1:
            win_prob = caller_distr.sum_where(lambda hand : hand < state.bettor_hand)
            loss_prob = caller_distr.sum_where(lambda hand : hand > state.bettor_hand)
            ev = (win_prob - loss_prob) * (state.pot()//2)
            return ev
        else:
            raise ValueError("Game over")
        
def FourCardRunout(bettor: FourCardBettor, caller: FourCardCaller, bettor_hand=None, caller_hand=None, revealed_card=None, streets=2):
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
    while not state.over and state.street() < streets:
        bettor_action = bettor.get_action(state)
        caller_action = caller.get_action(state)
        state.apply_actions(bettor_action, caller_action)
        print(state)
    return state