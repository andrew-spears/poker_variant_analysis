# %%
from game_utils2.core.game import SequentialGame
from game_utils2.core.strategy import Strategy, StrategyProfile
from game_utils2.solvers.CFR import CFRSolver
import numpy as np
from game_utils2.visualization.plotting import strategy_heatmaps, plot_cfr_regret_timeline, plot_action_likelihood_by_type
import matplotlib.pyplot as plt

# %%
kuhn = SequentialGame(
    actions=lambda hist: ["bet", "check"] if len(hist) == 0 else ["call", "fold"],
    player=lambda hist: len(hist) % 2,
    types=lambda: tuple(np.random.choice([0, 1, 2], size=2, replace=False)),
    terminal=lambda hist: len(hist) > 0 and hist[-1] in ['check', 'call', 'fold'],
    payoff=lambda hist, card0, card1: (
        0.5 if hist[-1] == 'fold' else
        1.5 * (1 if card0 > card1 else -1) if hist[-1] == 'call' else
        0.5 * (1 if card0 > card1 else -1)
    )
)

kuhnSolver = CFRSolver(kuhn, lambda_reg=0)
kuhnSolver.train(10000)
kuhnStrategy = kuhnSolver.get_strategy()

info_sets = kuhnSolver.get_info_sets()
plot_cfr_regret_timeline(kuhnSolver)
strategy_heatmaps(kuhnStrategy, info_sets, annotate=True)


# %%
def FBCP(bet_size, type_intervals=101): 
    return SequentialGame(
        actions=lambda hist: ["bet", "check"] if len(hist)==0 else ["call", "fold"],
        player=lambda hist: len(hist) % 2,
        types=lambda: tuple(np.random.choice(np.linspace(0, 1, type_intervals), size=2, replace=False)),
        terminal=lambda hist: len(hist) > 0 and hist[-1] in ['check', 'call', 'fold'],
        payoff=lambda hist, card0, card1: (
            0.5 if hist[-1] == 'fold' else
            (bet_size + 0.5) * (1 if card0 > card1 else -1) if hist[-1] == 'call' else
            0.5 * (1 if card0 > card1 else -1)
        )
    )

game = FBCP(1)
always_bet = Strategy(game, lambda hist, type : {"bet": 1})
always_check = Strategy(game, lambda hist, type : {"check": 1})
always_call = Strategy(game, lambda hist, type : {"call": 1})
profile = StrategyProfile(game, always_check, always_call)
profile.sample_outcome()

# %%
type_intervals = 51
FBCPSolver = CFRSolver(FBCP(1, type_intervals=type_intervals))
FBCPSolver.train(100000)
FBCPStrategy = FBCPSolver.get_strategy()
plot_cfr_regret_timeline(FBCPSolver, log_scale=True)
strategy_heatmaps(FBCPStrategy, FBCPSolver.get_info_sets(), annotate=False)

# %%
FBCPSolverReg = CFRSolver(FBCP(1, type_intervals=type_intervals), lambda_reg=0.1)
FBCPSolverReg.train(100000)
FBCPStrategyReg = FBCPSolverReg.get_strategy()

info_sets = FBCPSolver.get_info_sets()
strategy_heatmaps(FBCPStrategy, info_sets)
strategy_heatmaps(FBCPStrategyReg, info_sets)
# plot_cfr_regret_timeline(kuhnSolver)
# plot_action_likelihood_by_type(kuhnStrategyReg, (), "bet", info_sets)


# %%
def LCP(L, U, type_intervals=101, bet_size_intervals=101): 
    return SequentialGame(
        actions=lambda hist: np.concat([[0], np.linspace(L, U, bet_size_intervals)]) if len(hist)==0 else ["call", "fold"],
        player=lambda hist: len(hist) % 2,
        types=lambda: tuple(np.random.choice(np.linspace(0, 1, type_intervals), size=2, replace=False)),
        terminal=lambda hist: False if (len(hist) == 0) else (len(hist)== 2 or hist[0] == 0),
        payoff=lambda hist, x, y: (
            0.5 if hist[-1] == 'fold' else
            (hist[0] + 0.5) * (1 if x > y else -1) if hist[-1] == 'call' else
            0.5 * (1 if x > y else -1)
        )
    )

game = LCP(1, 2)
possible_bets = game.get_actions(())
bets = game.get_actions(())
random_bet = Strategy(game, lambda hist, type : {s: 1/len(bets) for s in bets})
always_check = Strategy(game, lambda hist, type : {0: 1})
always_call = Strategy(game, lambda hist, type : {"call": 1})
profile = StrategyProfile(game, random_bet, always_call)
profile.sample_outcome()

# %%
L, U = 0.5, 1.5
type_intervals = 51
bet_size_intervals = 11
game = LCP(L, U, type_intervals=type_intervals, bet_size_intervals=bet_size_intervals)
LCPSolver = CFRSolver(game, lambda_reg=0.02)

def calling_freq_heatmap(strategy, calling_info_sets):
    bets = sorted(list(set([h[0] for h, t in calling_info_sets])), reverse=True)
    types = sorted(list(set([t for h, t in calling_info_sets])))

    calling_freqs = np.zeros((len(bets), len(types)))
    for i, s in enumerate(bets):
        for j, t in enumerate(types):
            hist = (s,)
            freqs = strategy.get_freqs(hist, t)
            calling_freqs[i, j] = freqs["call"]

    fig, ax = plt.subplots(figsize=(10, 6))
    im = ax.imshow(calling_freqs, aspect="auto", cmap="YlOrRd", vmin=0, vmax=1)

    ax.set_xlabel("Hand Strength")
    ax.set_ylabel("Bet Size")
    ax.set_title("Calling Frequency vs Bet Size and Hand Strength")

    # Set y-axis labels (bet sizes)
    bet_labels = [f"{s:.2f}" for s in bets]
    ax.set_yticks(range(len(bets)))
    ax.set_yticklabels(bet_labels)

    # Set x-axis labels (hand types)
    type_ticks = [0, len(types) // 2, len(types) - 1]
    type_labels = [f"{types[i]:.2f}" for i in type_ticks]
    ax.set_xticks(type_ticks)
    ax.set_xticklabels(type_labels)

    # Add colorbar
    cbar = plt.colorbar(im, ax=ax)
    cbar.set_label("Call Probability")

    plt.tight_layout()
    plt.show()

#%%
LCPSolver.train(50000)
strategy = LCPSolver.get_strategy()

info_sets = LCPSolver.get_info_sets()
betting = [(h, t) for h, t in info_sets if len(h)==0]
strategy_heatmaps(strategy, betting, annotate=False)
calling = [(h, t) for h, t in info_sets if len(h)==1 and h!=(0)]
calling_freq_heatmap(strategy, calling)
plot_cfr_regret_timeline(LCPSolver, log_scale=True)


# %%
plot_action_likelihood_by_type(strategy, (), 1.0, info_sets)
