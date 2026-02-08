from typing import Tuple
import numpy as np
import matplotlib.pyplot as plt
from game_utils2.core.strategy import Strategy


def plot_cfr_regret_timeline(solver, log_scale=False):
    """Plot average regret vs iteration for both players."""
    regret_log = solver.get_regret_log()
    if not regret_log:
        print("No regret log data available")
        return

    iterations = np.array([item[0] for item in regret_log])
    regrets = np.array([item[1] for item in regret_log])

    plt.figure(figsize=(7, 4))
    plt.plot(iterations, regrets[:, 0], label='Player 0', linewidth=2)
    plt.plot(iterations, regrets[:, 1], label='Player 1', linewidth=2)
    plt.xlabel("Iteration")
    plt.ylabel("Average Regret")
    plt.title("CFR Training: Average Regret per Player")

    if log_scale:
        plt.yscale('log')

    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.show()


def plot_action_likelihood_by_type(strategy: Strategy, history, action, info_sets, annotate=False):
    """Bar plot showing probability of a specific action by type at given history."""
    types = sorted(list(set(t for h, t in info_sets if h == history)))
    if len(types) == 0:
        raise ValueError("No types found - maybe history not in info sets?")

    likelihoods = [strategy.get_freqs(history, t).get(action, 0) for t in types]

    fig, ax = plt.subplots(figsize=(12, 6))
    type_labels = [f"{t:.3g}" if isinstance(t, (int, float)) else str(t) for t in types]
    bars = ax.bar(range(len(types)), likelihoods, color='steelblue', alpha=0.7, edgecolor='black')

    if annotate:
        for bar, likelihood in zip(bars, likelihoods):
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height, f'{likelihood:.3f}',
                    ha='center', va='bottom', fontsize=10)

    ax.set_xlabel("Type", fontsize=12)
    ax.set_ylabel("Probability of Action", fontsize=12)
    ax.set_title(f"Likelihood of Action '{action}' at History '{history}'", fontsize=14)

    num_ticks = min(11, len(types))
    tick_positions = np.linspace(0, len(types) - 1, num_ticks, dtype=int)
    ax.set_xticks(tick_positions)
    ax.set_xticklabels([type_labels[i] for i in tick_positions], ha='right')

    ax.set_ylim(0, 1.1)
    ax.grid(True, axis='y', alpha=0.3)
    plt.tight_layout()
    plt.show()


def strategy_heatmaps(strategy: Strategy, info_sets, annotate=False, show_avg_action=True):
    """Plot strategy heatmaps showing action probabilities by type for each history."""
    histories = set(h for h, t in info_sets)
    num_histories = len(histories)
    fig, axes = plt.subplots(1, num_histories, figsize=(12, 5))

    if num_histories == 1:
        axes = [axes]

    for ax_idx, history in enumerate(histories):
        types = sorted(list(set(t for h, t in info_sets if h == history)))
        possible_actions = sorted(strategy.game.get_actions(history), reverse=True)
        heatmap_data = np.zeros((len(possible_actions), len(types)))

        for type_idx, type_val in enumerate(types):
            freqs = strategy.get_freqs(history, type_val)
            for action_idx, action in enumerate(possible_actions):
                heatmap_data[action_idx, type_idx] = freqs.get(action, 0)

        im = axes[ax_idx].imshow(heatmap_data, aspect="auto", cmap="YlOrRd", vmin=0, vmax=1)
        axes[ax_idx].set_xlabel("Type")
        axes[ax_idx].set_ylabel("Action")
        axes[ax_idx].set_title(f"Strategy for history: {history}")

        action_labels = [str(np.round(a, 3)) if isinstance(a, (int, float)) else a for a in possible_actions]
        axes[ax_idx].set_yticks(range(len(possible_actions)))
        axes[ax_idx].set_yticklabels(action_labels)

        type_ticks = [0, len(types) // 2, len(types) - 1]
        type_labels = [f"{types[i]:.2f}" for i in type_ticks]
        axes[ax_idx].set_xticks(type_ticks)
        axes[ax_idx].set_xticklabels(type_labels)

        if annotate:
            for i in range(heatmap_data.shape[0]):
                for j in range(heatmap_data.shape[1]):
                    value = heatmap_data[i, j]
                    text_color = 'white' if value > 0.5 else 'black'
                    axes[ax_idx].text(j, i, f'{value:.2f}', ha='center', va='center',
                                    color=text_color, fontsize=9)

        if show_avg_action:
            try:
                numerical_actions = sorted([float(a) for a in possible_actions])
                avg_actions = [sum(float(a) * strategy.get_freqs(history, t).get(a, 0)
                                  for a in possible_actions) for t in types]

                y_positions = []
                for avg_action in avg_actions:
                    if avg_action <= numerical_actions[0]:
                        y_pos = 0
                    elif avg_action >= numerical_actions[-1]:
                        y_pos = len(numerical_actions) - 1
                    else:
                        idx = np.searchsorted(numerical_actions, avg_action)
                        lower_action = numerical_actions[idx - 1]
                        upper_action = numerical_actions[idx]
                        frac = (avg_action - lower_action) / (upper_action - lower_action)
                        y_pos = (idx - 1) + frac

                    y_pos = len(numerical_actions) - 1 - y_pos
                    y_positions.append(y_pos)

                x_positions = np.arange(len(types))
                axes[ax_idx].plot(x_positions, y_positions, color='blue', linewidth=2.5,
                                 label='Avg Action', marker='o', markersize=6,
                                 markerfacecolor='lightblue', markeredgecolor='blue',
                                 markeredgewidth=1.5, zorder=10)
                axes[ax_idx].legend(loc='upper right')
            except (ValueError, TypeError):
                pass

        cbar = plt.colorbar(im, ax=axes[ax_idx])
        cbar.set_label("Probability")

    plt.tight_layout()
    plt.show()
