import numpy as np
from game_utils.ContinuousPokerVariants.ContinousPokerTemplate import ContinuousPokerTemplate

# NO LIMIT CONTINUOUS POKER
class NLCP(ContinuousPokerTemplate):
    @staticmethod
    def bluff_threshold():
        return 1 / 7

    @staticmethod
    def value_threshold():
        return 4 / 7

    @staticmethod
    def call_threshold(s):
        return 1 - 6 / (7 * (1 + s))

    @staticmethod
    def bluff_size(x):
        return (1 / (7 * x)**(1/3)) - 1

    @staticmethod
    def value_size(x):
        return np.sqrt(3 / (7 * (1 - x))) - 1
    
    @classmethod
    def generate_strategy_plot(cls, s_lim=None, grid_size=1001, save_path=None, title=None):
        # no game params for this variant
        super().generate_strategy_plot(s_lim=s_lim, grid_size=grid_size, save_path=save_path, title=title)