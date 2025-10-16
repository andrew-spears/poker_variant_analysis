import numpy as np

class ProgressiveKuhnPoker:
    '''
    n-card Kuhn poker where a remaining card from the deck is publicly revealed after each betting round.
    '''
    def __init__(self, n):
        self.cards = list(range(n))  # n-card deck
        self.reset()

    def reset(self):
        """ Shuffle and deal new cards """
        np.random.shuffle(self.cards)
        self.history = ""

    def get_current_player(self, history):
        """ Return the current player (0 = P1, 1 = P2) """
        return len(history) % 2

    def get_info_set(self, history):
        """ Return information set (what a player 'sees') """
        player = self.get_current_player(history)
        return (self.cards[player], history)

    def get_actions(self, history):
        """ Available actions at a given history """
        if history in ["B", "BC", "BFC", "BF"]:
            return []  # Terminal states
        return ["C", "B"] if history == "" or history[-1] == "C" else ["F", "C"]

    def get_next_state(self, history, action):
        """ Return next game state given action """
        return history + action

    def is_terminal(self, history):
        """ Check if the game has reached a terminal state """
        return history in ['BC', 'BFC', 'BF']

    def get_payoff(self, history):
        """ Compute payoff at terminal states """
        if not self.is_terminal(history):
            raise ValueError("Game is not in a terminal state")
        if history == "BF":
            return 1 if self.get_current_player(history) == 1 else -1
        return 1 if self.cards[0] > self.cards[1] else -1
