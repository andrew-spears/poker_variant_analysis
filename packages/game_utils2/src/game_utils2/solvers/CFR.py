import numpy as np
import random
import sys, os
import time
from game_utils2.core.game import SequentialGame, SequentialGameState
from game_utils2.core.strategy import Strategy


class Node:  # one per info set
    def __init__(self, actions, init_regret=0.01, epsilon=0.02):
        n = len(actions)
        self.actions = actions
        # CFR+ style nonnegative regret sums (start slightly positive = optimistic init)
        self.regret_sum = np.ones(n) * init_regret
        # stored behavioural strategy (after regret matching + exploration)
        self.strategy = np.ones(n) / n
        # accumulated (for average strategy)
        self.strategy_sum = np.zeros(n)
        # meta
        self.visits = 0
        self.epsilon = epsilon

    def __str__(self):
        return f"Node(visits={self.visits}, Regret: {np.round(self.regret_sum, 4)}, Strategy: {np.round(self.strategy, 4)}, Strategy Sum: {np.round(self.strategy_sum, 4)})"

    def __repr__(self):
        return str(self)

    def regret_match_base(self):
        """Regret-matching base (non-negative). Does NOT mix epsilon here."""
        pos = np.maximum(self.regret_sum, 0.0)
        pos_sum = np.sum(pos)
        if pos_sum > 0:
            return pos / pos_sum
        else:
            return np.ones(len(pos), dtype=self.regret_sum.dtype) / len(pos)

    def regret_match_strategy(self):
        """Return behavioural strategy = (1-eps)*RM + eps/uniform"""
        base = self.regret_match_base()
        n = len(base)
        eps = self.epsilon
        strat = (1.0 - eps) * base + eps / n
        # numerical safety
        strat = np.maximum(strat, 0.0)
        if strat.sum() == 0:
            strat = np.ones(n) / n
        else:
            strat = strat / strat.sum()
        return strat

    def get_average_strategy(self):
        """ Compute the average strategy over iterations.
        Safe if strategy_sum is all zeros.
        """
        ssum = np.sum(self.strategy_sum)
        if ssum <= 0:
            return np.ones_like(self.strategy_sum) / len(self.strategy_sum)
        return self.strategy_sum / ssum


class CFRSolver:
    """
    CFR+ with epsilon exploration and optimistic initialization. 
    Set epsilon=0 for vanilla CFR, 0.02 is good for some exploration.
    Set lambda_reg=0 for vanilla CFR, positive to regularize towards pure strategies by penalizing high entropy
    """
    def __init__(self, game: SequentialGame, epsilon=0, lambda_reg=0, init_regret=0.01):
        self.game = game
        self.node_map = {}  # maps info sets to nodes
        self.epsilon = epsilon
        self.lambda_reg = lambda_reg
        self.init_regret = init_regret
        self.iterations = 0
        self.regret_log = []  # List of (iteration, [regret_p0, regret_p1]) tuples

    def _get_node(self, state: SequentialGameState):
        curr_player = state.get_player()
        info_set = (state.history, state.types[curr_player])
        if info_set not in self.node_map:
            self.node_map[info_set] = Node(state.get_actions(), init_regret=self.init_regret, epsilon=self.epsilon)
        return self.node_map[info_set], info_set

    def _cfr_update(self, player, state: SequentialGameState, reach_probs):
        """
        Do one full (deterministic) traversal updating CFR+ regrets.
        Note: we keep full traversal (not sampled) but ensure exploration via epsilon mixing.
        """
        curr_player = state.get_player()

        # Terminal condition - return payoff of the node for the updating player
        if state.is_terminal():
            payoff = state.get_payoff()
            return payoff if player == 0 else -payoff

        node, info_set = self._get_node(state)
        node.visits += 1  # track visits (for monitoring / targeted exploration)
        # get behavioural strategy with epsilon
        strategy = node.regret_match_strategy()
        node.strategy = strategy.copy()  # store last behaviour strategy

        actions = state.get_actions()
        n = len(actions)
        action_values = np.zeros(n)

        # For each action, recurse
        for i, action in enumerate(actions):
            next_state = state.play_action(action)
            # Optimization: avoid copying array if we can reuse it
            reach_probs_next = reach_probs.copy()
            reach_probs_next[curr_player] *= strategy[i]
            action_values[i] = self._cfr_update(player, next_state, reach_probs_next)

        strategy_value = np.dot(strategy, action_values)

        # Compute counterfactual regret, only if updating player's node
        if player == curr_player:
            total_reach_prob = 1.0
            for j in range(len(reach_probs)):
                if j != player:
                    total_reach_prob *= reach_probs[j]

            # Update regrets: scale by counterfactual reach probability
            regret = action_values - strategy_value

            # Entropy regularization: subtract gradient of entropy to encourage pure strategies 
            # entropy of strategy is H(p) = -sum (p_i log(p_i))
            # gradient is -log(p) - 1
            regret += self.lambda_reg * (np.log(strategy+1e-9) + 1)

            # update node regret sum
            node.regret_sum = np.maximum(node.regret_sum + regret * total_reach_prob, 0.0)

            # Update average strategy sum using the reach probability of updating player
            node.strategy_sum += reach_probs[player] * node.strategy

        return strategy_value
    
    def average_regret(self):
        """
        Compute average positive counterfactual regret per player.
        This measures how far each player is from no-regret learning.
        """
        total = [0.0, 0.0]
        counts = [0, 0]

        for (hist, t), node in self.node_map.items():
            # Determine which player's infoset this node belongs to.
            # Assuming alternating turns: even len(hist) -> player 0, odd -> player 1.
            player = len(hist) % 2
            total[player] += np.sum(np.maximum(node.regret_sum, 0))
            counts[player] += len(node.regret_sum)

        # Avoid division by zero
        avg = []
        for i in [0, 1]:
            if counts[i] > 0 and self.iterations > 0:
                avg.append(total[i] / counts[i] / self.iterations)
            else:
                avg.append(0.0)
        return avg

    def train_step(self):
        for player in [0, 1]:
            state = self.game.get_instance()
            reach_probs = np.ones(2)
            self._cfr_update(player, state, reach_probs)


    def train(self, iterations, verbose=True, log_interval=10):
        """Run CFR for `iterations`. Each iteration runs one full traversal per player."""
        start_time = time.time()

        for it in range(1, iterations + 1):
            self.train_step()
            self.iterations += 1

            if it % log_interval == 0:
                # Store (iteration_number, [regret_p0, regret_p1]) tuple
                self.regret_log.append((self.iterations, self.average_regret()))

            # Progress reporting with timing
            checkpoint = max(1, iterations // 10)
            if verbose and (it % checkpoint == 0 or it == iterations):
                elapsed = time.time() - start_time
                rate = it / elapsed if elapsed > 0 else 0
                remaining = iterations - it
                eta = remaining / rate if rate > 0 else 0

                print(f"  Iteration {it:6d}/{iterations}: "
                      f"elapsed: {elapsed:7.2f}s, "
                      f"rate: {rate:6.1f} it/s, "
                      f"ETA: {eta:7.2f}s | "
                      f"infosets: {len(self.node_map)}")

        total_time = time.time() - start_time
        final_rate = iterations / total_time if total_time > 0 else 0

        if verbose:
            print(f"\nTraining complete!")
            print(f"  Total time: {total_time:.2f}s")
            print(f"  Average rate: {final_rate:.1f} iterations/s")


    def get_strategy(self):
        """ Return the learned strategy as a Strategy object"""
        def get_action_freqs(hist, type_):
            actions = self.game.get_actions(hist)
            freqs = self.node_map[(hist, type_)].get_average_strategy()
            return {a: f for a, f in zip(actions, freqs)}
        return Strategy(self.game, get_action_freqs)
    
    def get_regret_log(self):
        return self.regret_log

    def get_info_sets(self):
        return self.node_map.keys()

    def get_visit_stats(self):
        """Return a dict mapping info_set -> visits (useful to find under-visited states)"""
        return {info: node.visits for info, node in self.node_map.items()}
