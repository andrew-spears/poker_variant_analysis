from game_utils.ContinuousPokerVariants.ContinousPokerTemplate import ContinuousPokerTemplate

# FIXED BET CONTINUOUS POKER 

class FBCP(ContinuousPokerTemplate):
    # ---- Threshold functions ----
       
    @staticmethod
    def bluff_threshold(B):
        return 2 * B / ((1 + 2 * B) * (4 + 2 * B))

    @staticmethod
    def value_threshold(B):
        return (2 + 8 * B + 4 * B**2) / ((1 + 2 * B) * (4 + 2 * B))

    @staticmethod
    def call_threshold(s, B=None):
        return (2 * s * (3 + 2 * s)) / ((1 + 2 * s) * (4 + 2 * s))

    @staticmethod
    def bluff_size(x, B):
        return B

    @staticmethod
    def value_size(x, B):
        return B