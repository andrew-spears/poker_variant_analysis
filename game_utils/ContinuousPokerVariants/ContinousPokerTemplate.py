import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import TwoSlopeNorm

# TEMPLATE CLASS
class ContinuousPokerTemplate:
    @staticmethod
    def value_size(x, **kwargs):
        raise NotImplementedError("value_size method must be implemented in subclasses")
    
    @staticmethod
    def bluff_size(x, **kwargs):
        raise NotImplementedError("bluff_size method must be implemented in subclasses")

    @staticmethod
    def call_threshold(s, **kwargs):
        raise NotImplementedError("call_threshold method must be implemented in subclasses")
    
    @staticmethod
    def bluff_threshold(**kwargs):
        raise NotImplementedError("bluff_threshold method must be implemented in subclasses")
    
    @staticmethod
    def value_threshold(**kwargs):
        raise NotImplementedError("value_threshold method must be implemented in subclasses")
    
    @staticmethod
    def lose_showdown_payoff(s_integral, area):
            return -s_integral - 0.5* area
        
    @staticmethod
    def win_showdown_payoff(s_integral, area):
        return s_integral + 0.5* area
    
    @staticmethod
    def lose_ante_payoff(_, area):
        return -area*0.5
    
    @staticmethod
    def win_ante_payoff(_, area):
        return area*0.5

    @staticmethod  
    def outcome_to_payoff(outcome, s):
        if outcome == "Bluff_Called":
            return ContinuousPokerTemplate.lose_showdown_payoff(s, 1)
        elif outcome == "Bluff_Fold":
            return ContinuousPokerTemplate.win_ante_payoff(0, 1)
        elif outcome == "Value_Fold":
            return ContinuousPokerTemplate.win_ante_payoff(0, 1)
        elif outcome == "Value_Loses":
            return ContinuousPokerTemplate.lose_showdown_payoff(s, 1)
        elif outcome == "Value_Wins":
            return ContinuousPokerTemplate.win_showdown_payoff(s, 1)
        elif outcome == "Check_Wins":
            return ContinuousPokerTemplate.win_ante_payoff(0, 1)
        elif outcome == "Check_Loses":
            return ContinuousPokerTemplate.lose_ante_payoff(0, 1)
        else:
            raise ValueError(f"Unknown outcome: {outcome}")

    @classmethod
    def payoff_outcome(cls, x, y, **kwargs):
        if x < cls.bluff_threshold(**kwargs): # bluff
            s = cls.bluff_size(x, **kwargs)
            if y > cls.call_threshold(s, **kwargs):
                outcome = "Bluff_Called"
            else:
                outcome = "Bluff_Fold"
        elif x > cls.value_threshold(**kwargs): # value bet
            s = cls.value_size(x, **kwargs)
            if y < cls.call_threshold(s, **kwargs):
                outcome = "Value_Fold"
            elif y > x:
                outcome = "Value_Loses"
            else:
                outcome = "Value_Wins"
        else: 
            s=0
            if x > y:
                outcome = "Check_Wins" 
            else:
                outcome = "Check_Loses"
        return cls.outcome_to_payoff(outcome, s), outcome
            
    @classmethod
    def expected_payoff(cls, grid_size=1001, **kwargs):
        # numerically integrate the payoff(x, y) function over the grid [0,1] x [0,1]
        xs = np.linspace(0, 1, grid_size)
        ys = np.linspace(0, 1, grid_size)
        payoff_data = np.empty((grid_size, grid_size))
        for i in range(grid_size):
            for j in range(grid_size):
                try:
                    val, _ = cls.payoff_outcome(xs[i], ys[j], **kwargs)
                    payoff_data[i, j] = val if np.isfinite(val) else np.nan
                except:
                    payoff_data[i, j] = np.nan
        average_payoff = np.nanmean(payoff_data)
        return average_payoff
    
    @classmethod
    def total_payoff_for_outcome(cls, outcome, grid_size=1001, **kwargs):
        # numerically integrate the payoff(x, y) function over the grid [0,1] x [0,1], only where the outcome is outcome
        xs = np.linspace(0, 1, grid_size)
        ys = np.linspace(0, 1, grid_size)
        payoff_data = np.empty((grid_size, grid_size))
        for i in range(grid_size):
            for j in range(grid_size):
                try:
                    val, oc = cls.payoff_outcome(xs[i], ys[j], **kwargs)
                    if oc == outcome:
                        payoff_data[i, j] = val if np.isfinite(val) else np.nan
                    else:
                        payoff_data[i, j] = 0
                except:
                    payoff_data[i, j] = 0
        total_payoff = np.nanmean(payoff_data)
        return total_payoff

    @classmethod
    def generate_strategy_plot(cls, s_lim=None, grid_size=1001, save_path=None, title=None, **kwargs):
        # find bluff and value sizes for each x
        X = np.linspace(0, 1, grid_size)
        bet_sizes = np.empty(grid_size)
        call_thresholds = np.empty(grid_size)
        for i, x in enumerate(X):
            if x < cls.bluff_threshold(**kwargs):
                s = cls.bluff_size(x, **kwargs)
            elif x > cls.value_threshold(**kwargs):
                s = cls.value_size(x, **kwargs)
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
            call_thresholds[i] = cls.call_threshold(s, **kwargs)

        # plot
        fig, ax = plt.subplots(figsize=(8, 6))

        # Plot bet sizes as a function of x
        ax.plot(adjusted_X, adjusted_bet_sizes, label="Bet Function", color="red", linewidth=2)

        # Plot call thresholds as a function of s
        if s_min == s_max:
            # point instead of line
            ax.plot(call_thresholds, S, label="Call Threshold", color="blue", marker="o", markersize=5)
            ax.plot([call_thresholds[0], 1], [S[0], S[0]], color="blue", linestyle="--", alpha=0.3, linewidth=2, label="Call Region") 
        else:
            ax.plot(call_thresholds, S, label="Call Threshold", color="darkblue", linestyle="--", linewidth=2)
            ax.fill_betweenx(S, call_thresholds, np.ones_like(S), color="blue", alpha=0.3, label="Call Region")

        # ---- Labels, Legend, and Title ----
        if s_lim is None:
            s_lim = np.max(adjusted_bet_sizes) * 1.1
        ax.set_xlim(-0.05, 1.05)
        ax.set_ylim(-0.05, s_lim + 0.05)
        ax.set_xlabel("Hand Strength", fontsize=12)
        ax.set_ylabel("Bet Size", fontsize=12)

        if title is None:
            title = f"{cls.__name__} Strategy Profile"
            if kwargs:
                kwargs_str = ", ".join([f"{k}={v}" for k, v in kwargs.items()])
                title += f" with {kwargs_str}"
        ax.set_title(title, fontsize=14)
        ax.legend(fontsize=10)
        ax.grid(True)

        # ---- Save or Show ----
        plt.tight_layout()
        if save_path:
            plt.savefig(save_path, dpi=300)
        plt.show()


    @classmethod
    def generate_payoff_plot(cls, grid_size=1001, save_path=None, title="Payoffs by Hand Strength", **kwargs):
        # ---- Parameters ----
        xs = np.linspace(0, 1, grid_size)
        ys = np.linspace(0, 1, grid_size)
        X, Y = np.meshgrid(xs, ys, indexing='ij')
        color_cap = 2

        # ---- Compute payoff grid ----
        payoff_data = np.empty((grid_size, grid_size))
        outcome_type = np.empty((grid_size, grid_size), dtype=object)
        for i in range(grid_size):
            for j in range(grid_size):
                try:
                    val, outcome = cls.payoff_outcome(xs[i], ys[j], **kwargs)
                    payoff_data[i, j] = val if np.isfinite(val) else np.nan
                    outcome_type[i, j] = outcome
                except:
                    payoff_data[i, j] = np.nan
        payoff_clipped = np.clip(payoff_data, -color_cap, color_cap)

        region_labels = [
            "Bluff_Called", "Bluff_Fold",
            "Value_Wins", "Value_Loses", "Value_Fold",
            "Check_Wins", "Check_Loses"
        ]

        # ---- Plot heatmap with region contours and labels ----
        fig, ax = plt.subplots(figsize=(7, 7))
        c = ax.imshow(
            payoff_clipped.T,
            extent=[0, 1, 0, 1],
            origin='lower',
            cmap='coolwarm',
            norm=TwoSlopeNorm(vmin=-color_cap, vcenter=0, vmax=color_cap)
        )
        cbar = fig.colorbar(c, ax=ax, shrink=0.9)
        cbar.set_label("Bettor Payoff", fontsize=12)
        cbar.set_ticks([-color_cap, 0, color_cap])
        cbar.set_ticklabels([f"<-{color_cap}", "0", f">{color_cap}"])

        for label in region_labels:
            mask = outcome_type == label
            if np.any(mask):
                ax.contour(
                    X, Y, mask.astype(float),
                    levels=[0.5],
                    colors='white',
                    linewidths=1.5
                )
                region_center = np.argwhere(mask)
                if len(region_center) > 0:
                    center_x, center_y = region_center.mean(axis=0)
                    ax.text(
                        xs[int(center_x)], ys[int(center_y)],
                        label.replace("_", " "),
                        color="white",
                        fontsize=10,
                        ha="center",
                        va="center",
                        bbox=dict(facecolor="black", alpha=0.5, edgecolor="none")
                    )

        ax.set_xlabel("x (bettor hand strength)")
        ax.set_ylabel("y (caller hand strength)")
        ax.set_title(title)
        plt.tight_layout()
        if save_path is not None:
            plt.savefig(save_path, dpi=300)
        plt.show()