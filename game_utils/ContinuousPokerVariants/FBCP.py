from game_utils.ContinuousPokerVariants.ContinousPokerTemplate import ContinuousPokerTemplate

# FIXED BET CONTINUOUS POKER 

class FBCP(ContinuousPokerTemplate):
    # ---- Threshold functions ----
       
    def bluff_threshold(game_params):
        B = game_params['B']
        return 2 * B / ((1 + 2 * B) * (4 + 2 * B))

    def value_threshold(game_params):
        B = game_params['B']
        return (2 + 8 * B + 4 * B**2) / ((1 + 2 * B) * (4 + 2 * B))

    def call_threshold(game_params, s):
        return (2 * s * (3 + 2 * s)) / ((1 + 2 * s) * (4 + 2 * s))

    def bluff_size(game_params, x):
        return game_params['B']

    def value_size(game_params, x):
        return game_params['B']