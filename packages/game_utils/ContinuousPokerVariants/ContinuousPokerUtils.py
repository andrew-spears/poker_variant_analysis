import numpy as np
import matplotlib.pyplot as plt


def generate_strategy_plot(
    bluff_threshold,
    bluff_size,
    value_threshold,
    value_size,
    call_threshold,
    s_lim=None,
    grid_size=1001,
    save_path=None,
    title="Strategy Plot",
    **kwargs
):
    """
    The parameters of the game should be in kwargs (will be passed to all strategy functions).
    """
    # find bluff and value sizes for each x
    X = np.linspace(0, 1, grid_size)
    bet_sizes = np.empty(grid_size)
    call_thresholds = np.empty(grid_size)
    for i, x in enumerate(X):
        if x < bluff_threshold(**kwargs):
            s = bluff_size(x, **kwargs)
        elif x > value_threshold(**kwargs):
            s = value_size(x, **kwargs)
        else:
            s = 0
        bet_sizes[i] = s

    # Add artificial points for perfect vertical lines
    adjusted_X = []
    adjusted_bet_sizes = []
    for i in range(len(bet_sizes) - 1):
        adjusted_X.append(X[i])
        adjusted_bet_sizes.append(bet_sizes[i])
        if bet_sizes[i] != 0 and bet_sizes[i + 1] == 0:
            adjusted_X.append(X[i])
            adjusted_bet_sizes.append(0)
        elif bet_sizes[i] == 0 and bet_sizes[i + 1] != 0:
            adjusted_X.append(X[i + 1])
            adjusted_bet_sizes.append(0)
    adjusted_X.append(X[-1])
    adjusted_bet_sizes.append(bet_sizes[-1])

    adjusted_X = np.array(adjusted_X)
    adjusted_bet_sizes = np.array(adjusted_bet_sizes)

    # find call thresholds for each s
    s_min = np.min(adjusted_bet_sizes[adjusted_bet_sizes > 0])
    s_max = np.max(adjusted_bet_sizes[adjusted_bet_sizes != np.inf])
    S = np.linspace(s_min, s_max, grid_size)
    for i, s in enumerate(S):
        call_thresholds[i] = call_threshold(s, **kwargs)

    # plot
    fig, ax = plt.subplots(figsize=(8, 6))

    # Plot bet sizes as a function of x
    ax.plot(
        adjusted_X, adjusted_bet_sizes, label="Bet Function", color="red", linewidth=2
    )

    # Plot call thresholds as a function of s
    if s_min == s_max:
        # point instead of line
        ax.plot(
            call_thresholds,
            S,
            label="Call Threshold",
            color="blue",
            marker="o",
            markersize=5,
        )
        ax.plot(
            [call_thresholds[0], 1],
            [S[0], S[0]],
            color="blue",
            linestyle="--",
            alpha=0.3,
            linewidth=2,
            label="Call Region",
        )
    else:
        ax.plot(
            call_thresholds,
            S,
            label="Call Threshold",
            color="darkblue",
            linestyle="--",
            linewidth=2,
        )
        ax.fill_betweenx(
            S,
            call_thresholds,
            np.ones_like(S),
            color="blue",
            alpha=0.3,
            label="Call Region",
        )

    # ---- Labels, Legend, and Title ----
    if s_lim is None:
        s_lim = np.max(adjusted_bet_sizes) * 1.1
    ax.set_xlim(-0.05, 1.05)
    ax.set_ylim(-0.05, s_lim + 0.05)
    ax.set_xlabel("Hand Strength", fontsize=12)
    ax.set_ylabel("Bet Size", fontsize=12)

    ax.set_title(title, fontsize=14)
    ax.legend(fontsize=10)
    ax.grid(True)

    # ---- Save or Show ----
    plt.tight_layout()
    if save_path:
        plt.savefig(save_path, dpi=300)
    plt.show()
