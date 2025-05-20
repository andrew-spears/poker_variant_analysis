import numpy as np
from game_utils.ContinuousPokerVariants.ContinousPokerTemplate import ContinuousPokerTemplate

# NO LIMIT CONTINUOUS POKER
class NLCP(ContinuousPokerTemplate):
    def bluff_threshold(game_params):
        return 1 / 7

    def value_threshold(game_params):
        return 4 / 7

    def call_threshold(game_params, s):
        return 1 - 6 / (7 * (1 + s))

    def bluff_size(game_params, x):
        return (1 / (7 * x)**(1/3)) - 1

    def value_size(game_params, x):
        return np.sqrt(3 / (7 * (1 - x))) - 1