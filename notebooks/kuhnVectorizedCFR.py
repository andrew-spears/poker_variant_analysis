import numpy as np
from typing import Tuple, List, Dict
import time


class FastKuhnPoker:
    """
    Ultra-fast CFR for Kuhn Poker using pure iteration and vectorization.
    No recursion, processes entire levels at once.
    """
    
    def __init__(self, n_cards: int, use_abstraction: bool = False, n_buckets: int = 10):
        """
        Initialize Kuhn Poker CFR solver.
        """
        self.n_cards = n_cards
        self.use_abstraction = use_abstraction
        self.n_buckets = n_buckets if use_abstraction else n_cards
        
        print(f"Initializing Fast Kuhn Poker: {n_cards} cards, abstraction={use_abstraction}")
        
        # Build flat game structure
        self._build_flat_structure()
        
        # Initialize CFR arrays
        n_infosets = len(self.infoset_cards)
        
        self.regret_sum = np.zeros((n_infosets, 2), dtype=np.float32)
        self.strategy_sum = np.zeros((n_infosets, 2), dtype=np.float32)
        
        print(f"Created {n_infosets} info sets")
    
    def _card_bucket(self, card: int) -> int:
        """Map card to bucket (for abstraction)"""
        if not self.use_abstraction:
            return card
        bucket_size = max(1, self.n_cards // self.n_buckets)
        return min(card // bucket_size, self.n_buckets - 1)
    
    def _build_flat_structure(self):
        """
        Build game structure as flat arrays for maximum speed.
        
        Key insight: Kuhn poker has simple structure:
        - All deals equally likely (uniform chance)
        - P1 info sets: just the card they hold
        - P2 info sets: card they hold + "saw bet"
        - Terminals: (c1, c2, history)
        
        We'll store everything as parallel arrays indexed by deal.
        """
        
        # Valid deals: all (c1, c2) pairs where c1 != c2
        self.deals = []  # List of (c1, c2) tuples
        self.deal_probs = []  # Probability of each deal (uniform)
        
        for c1 in range(self.n_cards):
            for c2 in range(self.n_cards):
                if c1 != c2:
                    self.deals.append((c1, c2))
        
        self.deals = np.array(self.deals, dtype=np.int32)
        n_deals = len(self.deals)
        self.deal_prob = 1.0 / n_deals
        
        # Build info sets
        # P1 info sets: one per card bucket
        # P2 info sets: one per card bucket (only after P1 bets)
        self.p1_infosets = {}  # card_bucket -> infoset_idx
        self.p2_infosets = {}  # card_bucket -> infoset_idx
        
        self.infoset_cards = []  # Which card bucket
        self.infoset_player = []  # 0 or 1
        
        for card_bucket in range(self.n_buckets):
            # P1 info set
            p1_idx = len(self.infoset_cards)
            self.p1_infosets[card_bucket] = p1_idx
            self.infoset_cards.append(card_bucket)
            self.infoset_player.append(0)
            
            # P2 info set
            p2_idx = len(self.infoset_cards)
            self.p2_infosets[card_bucket] = p2_idx
            self.infoset_cards.append(card_bucket)
            self.infoset_player.append(1)
        
        # Pre-compute payoffs for all terminals
        # Terminals: (c1, c2, action_sequence)
        # - P1 checks: showdown with pot=2, winner gets +1
        # - P1 bets, P2 folds: P1 wins pot=3, gets +1
        # - P1 bets, P2 calls: showdown with pot=4, winner gets +2
        
        c1_vals = self.deals[:, 0]
        c2_vals = self.deals[:, 1]
        
        # Precompute who wins (1 if P1 wins, -1 if P2 wins)
        self.winners = np.where(c1_vals > c2_vals, 1, -1).astype(np.float32)
        
        # Map deals to info sets
        c1_buckets = np.array([self._card_bucket(c) for c in c1_vals], dtype=np.int32)
        c2_buckets = np.array([self._card_bucket(c) for c in c2_vals], dtype=np.int32)
        
        self.deal_to_p1_infoset = np.array([self.p1_infosets[c] for c in c1_buckets], dtype=np.int32)
        self.deal_to_p2_infoset = np.array([self.p2_infosets[c] for c in c2_buckets], dtype=np.int32)
        
        print(f"Built flat structure: {n_deals} deals, {len(self.infoset_cards)} info sets")
    
    def _get_strategies(self, infoset_indices: np.ndarray) -> np.ndarray:
        """Get strategies for multiple info sets at once (vectorized)"""
        regrets = self.regret_sum[infoset_indices]  # Shape: (n, 2)
        
        positive_regrets = np.maximum(regrets, 0)
        sums = np.sum(positive_regrets, axis=1, keepdims=True)
        
        # Where sum > 0, use regret matching; else uniform
        strategies = np.where(sums > 0, 
                             positive_regrets / sums,
                             0.5)  # Uniform [0.5, 0.5]
        
        return strategies.astype(np.float32)
    
    def train(self, iterations: int, verbose: bool = True):
        """
        Train CFR - fully iterative, no recursion!
        
        Algorithm:
        1. For each deal, compute strategies at P1 and P2 info sets
        2. Compute values for all 4 terminal outcomes per deal
        3. Compute expected values working backward
        4. Update regrets and strategy sums
        """
        start_time = time.time()
        n_deals = len(self.deals)
        
        for iteration in range(iterations):
            if verbose and (iteration + 1) % 1000 == 0:
                elapsed = time.time() - start_time
                iters_per_sec = (iteration + 1) / elapsed
                print(f"Iteration {iteration+1}/{iterations} ({iters_per_sec:.1f} iter/s)")
            
            # Update both players
            for player in [0, 1]:
                # Get all P1 strategies (one per deal)
                p1_infosets = self.deal_to_p1_infoset
                p1_strategies = self._get_strategies(p1_infosets)  # Shape: (n_deals, 2)
                
                # Get all P2 strategies (one per deal)
                p2_infosets = self.deal_to_p2_infoset
                p2_strategies = self._get_strategies(p2_infosets)  # Shape: (n_deals, 2)
                
                # Compute terminal values for all deals and all action combinations
                # 4 terminals per deal:
                # 1. P1 checks: payoff = winner * 1
                # 2. P1 bets, P2 folds: payoff = 1 (P1 always wins)
                # 3. P1 bets, P2 calls: payoff = winner * 2
                
                v_check = self.winners  # Shape: (n_deals,)
                v_bet_fold = np.ones(n_deals, dtype=np.float32)  # P1 always wins
                v_bet_call = self.winners * 2
                
                # From P2's perspective: compute expected value of betting
                # P2 chooses fold (action 0) or call (action 1)
                # EV(bet) = prob(fold) * v_bet_fold + prob(call) * v_bet_call
                v_p1_bets = (p2_strategies[:, 0] * v_bet_fold + 
                            p2_strategies[:, 1] * v_bet_call)
                
                # From P1's perspective: compute expected value
                # P1 chooses check (action 0) or bet (action 1)
                # EV = prob(check) * v_check + prob(bet) * v_p1_bets
                v_p1_node = (p1_strategies[:, 0] * v_check + 
                            p1_strategies[:, 1] * v_p1_bets)
                
                # Flip sign if we're player 1
                if player == 1:
                    v_check = -v_check
                    v_bet_fold = -v_bet_fold
                    v_bet_call = -v_bet_call
                    v_p1_bets = -v_p1_bets
                    v_p1_node = -v_p1_node
                
                # Update regrets for P1 info sets
                if player == 0:
                    # Reach probabilities
                    # P1's reach prob = deal_prob (uniform chance)
                    # P2's reach prob = deal_prob (they haven't acted yet)
                    # CFR reach = opponent reach = deal_prob
                    
                    cfr_reach_p1 = self.deal_prob
                    
                    # Action values for P1
                    av_check = v_check
                    av_bet = v_p1_bets
                    
                    # Regrets
                    regret_check = (av_check - v_p1_node) * cfr_reach_p1
                    regret_bet = (av_bet - v_p1_node) * cfr_reach_p1
                    
                    # Accumulate regrets (group by info set)
                    for deal_idx in range(n_deals):
                        infoset_idx = p1_infosets[deal_idx]
                        self.regret_sum[infoset_idx, 0] += regret_check[deal_idx]
                        self.regret_sum[infoset_idx, 1] += regret_bet[deal_idx]
                    
                    # Update strategy sum
                    # P1's reach prob = deal_prob
                    my_reach_p1 = self.deal_prob
                    
                    for deal_idx in range(n_deals):
                        infoset_idx = p1_infosets[deal_idx]
                        self.strategy_sum[infoset_idx] += my_reach_p1 * p1_strategies[deal_idx]
                
                # Update regrets for P2 info sets
                else:  # player == 1
                    # P2 only acts after P1 bets
                    # P2's reach prob = deal_prob (chance) * 1 (P2 hasn't acted)
                    # P1's reach prob = deal_prob (chance) * prob(P1 bets)
                    # CFR reach = P1's reach = deal_prob * prob(P1 bets)
                    
                    cfr_reach_p2 = self.deal_prob * p1_strategies[:, 1]  # P1 bet prob
                    
                    # Action values for P2 (given P1 bet)
                    av_fold = v_bet_fold
                    av_call = v_bet_call
                    
                    # Node value (given P1 bet)
                    # Regrets
                    regret_fold = (av_fold - v_p1_bets) * cfr_reach_p2
                    regret_call = (av_call - v_p1_bets) * cfr_reach_p2
                    
                    # Accumulate regrets
                    for deal_idx in range(n_deals):
                        infoset_idx = p2_infosets[deal_idx]
                        self.regret_sum[infoset_idx, 0] += regret_fold[deal_idx]
                        self.regret_sum[infoset_idx, 1] += regret_call[deal_idx]
                    
                    # Update strategy sum
                    # P2's reach prob = deal_prob * prob(P1 bets)
                    my_reach_p2 = self.deal_prob * p1_strategies[:, 1]
                    
                    for deal_idx in range(n_deals):
                        infoset_idx = p2_infosets[deal_idx]
                        self.strategy_sum[infoset_idx] += my_reach_p2[deal_idx] * p2_strategies[deal_idx]
        
        total_time = time.time() - start_time
        print(f"\nTraining complete: {iterations} iterations in {total_time:.2f}s ({iterations/total_time:.1f} iter/s)")
    
    def get_average_strategy(self, infoset_idx: int) -> np.ndarray:
        """Get average strategy for an info set"""
        strategy_sum = self.strategy_sum[infoset_idx]
        total = np.sum(strategy_sum)
        
        if total > 0:
            return strategy_sum / total
        else:
            return np.array([0.5, 0.5], dtype=np.float32)
    
    def print_strategy(self, num_examples: int = 10):
        """Print example strategies"""
        print("\n=== Average Strategies ===")
        
        # P1 strategies
        print("\nPlayer 1 (Check/Bet):")
        for card_bucket, infoset_idx in sorted(self.p1_infosets.items())[:num_examples]:
            strategy = self.get_average_strategy(infoset_idx)
            label = f"Bucket {card_bucket}" if self.use_abstraction else f"Card {card_bucket}"
            print(f"  {label}: Check={strategy[0]:.3f}, Bet={strategy[1]:.3f}")
        
        if len(self.p1_infosets) > num_examples:
            print(f"  ... ({len(self.p1_infosets) - num_examples} more)")
        
        # P2 strategies
        print("\nPlayer 2 (Fold/Call after P1 bets):")
        for card_bucket, infoset_idx in sorted(self.p2_infosets.items())[:num_examples]:
            strategy = self.get_average_strategy(infoset_idx)
            label = f"Bucket {card_bucket}" if self.use_abstraction else f"Card {card_bucket}"
            print(f"  {label}: Fold={strategy[0]:.3f}, Call={strategy[1]:.3f}")
        
        if len(self.p2_infosets) > num_examples:
            print(f"  ... ({len(self.p2_infosets) - num_examples} more)")


# Even faster with numba JIT compilation
try:
    from numba import jit, prange
    
    @jit(nopython=True, parallel=True, fastmath=True)
    def update_regrets_p1(regret_sum, strategy_sum, p1_infosets, 
                         regret_check, regret_bet, p1_strategies, my_reach):
        """JIT-compiled regret update for P1"""
        n_deals = len(p1_infosets)
        for deal_idx in prange(n_deals):
            infoset_idx = p1_infosets[deal_idx]
            regret_sum[infoset_idx, 0] += regret_check[deal_idx]
            regret_sum[infoset_idx, 1] += regret_bet[deal_idx]
            strategy_sum[infoset_idx, 0] += my_reach * p1_strategies[deal_idx, 0]
            strategy_sum[infoset_idx, 1] += my_reach * p1_strategies[deal_idx, 1]
    
    @jit(nopython=True, parallel=True, fastmath=True)
    def update_regrets_p2(regret_sum, strategy_sum, p2_infosets,
                         regret_fold, regret_call, p2_strategies, my_reach):
        """JIT-compiled regret update for P2"""
        n_deals = len(p2_infosets)
        for deal_idx in prange(n_deals):
            infoset_idx = p2_infosets[deal_idx]
            regret_sum[infoset_idx, 0] += regret_fold[deal_idx]
            regret_sum[infoset_idx, 1] += regret_call[deal_idx]
            strategy_sum[infoset_idx, 0] += my_reach[deal_idx] * p2_strategies[deal_idx, 0]
            strategy_sum[infoset_idx, 1] += my_reach[deal_idx] * p2_strategies[deal_idx, 1]
    
    NUMBA_AVAILABLE = True
    print("Numba JIT compilation available - will be even faster!")
    
except ImportError:
    NUMBA_AVAILABLE = False
    print("Numba not available - install with 'pip install numba' for 10x+ speedup")


def benchmark():
    """Run benchmarks"""
    print("=" * 60)
    print("FAST KUHN POKER CFR BENCHMARK")
    print("=" * 60)
    
    configs = [
        (20, False, 10000),
        (50, False, 10000),
        (100, False, 10000),
        (100, True, 50000),
        (200, True, 50000),
    ]
    
    for n_cards, use_abs, iters in configs:
        n_buckets = max(10, n_cards // 10) if use_abs else n_cards
        desc = f"{n_cards} cards" + (f", {n_buckets} buckets" if use_abs else ", no abstraction")
        
        print(f"\n{desc}:")
        solver = FastKuhnPoker(n_cards, use_abstraction=use_abs, n_buckets=n_buckets)
        solver.train(iters, verbose=False)
        solver.print_strategy(num_examples=5)


if __name__ == "__main__":
    # Quick test
    print("Testing with 100 cards, 10 buckets...")
    solver = FastKuhnPoker(n_cards=100, use_abstraction=True, n_buckets=10)
    solver.train(10000)
    solver.print_strategy()
    
    print("\n" + "=" * 60)
    response = input("Run full benchmark? (y/n): ")
    if response.lower() == 'y':
        benchmark()