import numpy as np
import random
import sys, os
from game_utils.utils import normalize
# import seaborn as sns
import matplotlib.pyplot as plt
from game_utils.Strategy import MixedStrategy
from game_utils.ZeroSumGame import ZeroSumGame
from game_utils.InfoSet import InfoSet

class CFRSolver:
    """
    Counterfactual Regret Minimization (CFR) Solver for two-player zero-sum games.
    CFR is an iterative algorithm used to find approximate Nash equilibria in extensive-form games.
    It works by iteratively updating regret values for each decision point (information set) and 
    using these regrets to adjust the strategy towards better responses over time.
    
    Example usage:

    solver = CFR.CFRSolver(kuhn.ThreeCard) # initialize the solver for a specific game class
    solver.train(10000) # train for 10000 iterations
    combined_strat = solver.get_strategy(0) | solver.get_strategy(1) # combine both players' strategies into one strategy
    utils.binaryStrategyHeatmap(combined_strat, title="CFR Nash EQ")
    """
    def __init__(self, game_class: ZeroSumGame):
        self.game_class = game_class
        self.node_map = {}  # maps info sets to nodes

    class Node: # one per info set
        def __init__(self, num_actions):
            self.regret_sum = np.zeros(num_actions)  # Regret values for each action
            self.strategy = np.ones(num_actions) / num_actions  # Initial uniform strategy
            self.strategy_sum = np.zeros(num_actions)  # Sum of strategies over iterations

        def __str__(self):
            return f"Node with Regret: {np.round(self.regret_sum, 2)}, Strategy: {np.round(self.strategy, 2)}, Strategy Sum: {np.round(self.strategy_sum, 2)}"

        def __repr__(self):
            return str(self)

        def regret_match_strategy(self):
            """ for all actions, if the regret is positive, play that action more often. 
            Return a strategy based on this and add to strategy_sum """
            strategy = normalize(np.maximum(self.regret_sum, 0))
            return strategy

        def get_average_strategy(self):
            """ Compute the average strategy over iterations.
             Returns a numpy array of frequencies over actions at this info set.
               """
            return normalize(self.strategy_sum)

    def _cfr_update(self, player, state: ZeroSumGame, reach_probs):
        """ 
        do one iteration of CFR and update our regrets and strategy. 
        return the value of the state for the current player under the current strategy.
        player is the player who is updating (do nothing to our regrets if not the current player)
        reach_probs: an array of probabilities for each player to play to reach this state.
        """
        curr_player = state.current_player()

        # Terminal condition - return payoff of the node for the updating player
        if state.is_terminal():
            return state.get_payoff(player)
        
        # Get or create the node for this state
        info_set = state.current_info_set()
        if info_set not in self.node_map:
            self.node_map[info_set] = self.Node(len(state.get_actions()))
        node = self.node_map[info_set]

        # Get the regret-matched strategy and initialize our values for this iteration
        strategy = node.regret_match_strategy()
        strategy_value = 0 # the node value according to current strategy
        action_values = np.zeros(len(strategy)) # the node value if we chose this action

        # Counterfactual regret calculation
        for i, action in enumerate(state.get_actions()):
            next_state = state.get_next_state(action)
            reach_probs_next = reach_probs.copy()
            reach_probs_next[curr_player] *= strategy[i] # the curr player would have to take this action to reach the next state
            action_value = self._cfr_update(player, next_state, reach_probs_next)
            action_values[i] = action_value
        strategy_value = np.dot(strategy, action_values)

        # Compute counterfactual regret, if we are the current player
        if player == curr_player:
            regret = action_values - strategy_value

            # product of reach probs other than our own
            total_reach_prob = np.prod(reach_probs[np.arange(len(reach_probs)) != player])
            node.regret_sum += regret * total_reach_prob
            node.strategy = node.regret_match_strategy() # update the strategy for this node
            node.strategy_sum += reach_probs[player] * node.strategy

        return strategy_value

    def train(self, iterations):
        """ Run CFR for the specified number of iterations. initialize_game_func should return a new game state. """
        for _ in range(iterations):
            for player in [0, 1]:
                state = self.game_class.random()
                reach_probs = np.ones(2)
                self._cfr_update(player, state, reach_probs)

    def get_strategy(self, player):
        """ Return the learned strategy for the given player as a MixedStrategy object."""
        # node_map maps info sets to frequency arrays.
        infoSets = self.game_class.all_info_sets(player)
        return MixedStrategy({I: self.node_map[I].get_average_strategy() for I in infoSets}, self.game_class)
    