import numpy as np
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from game_utils.ZeroSumGame import ZeroSumGame


class MixedStrategy(dict):
    """
    a dict mapping InfoSets to arrays of action frequencies.
    """
    @classmethod
    def empty(cls, game: "ZeroSumGame", player):
        '''
        strategy with 0 probability of doing anything at any info set (not actually valid)
        '''
        strat = cls({}, game)
        infoSets = game.info_sets(player)
        for I in infoSets:
            actions = game.get_actions_at_info_set(I)
            strat[I] = np.zeros(len(actions))
        return strat
        
    @classmethod
    def from_normal_form(cls, frequencies: np.array, player, game: "ZeroSumGame"):
        '''
        normal_frequencies: a list of the frequencies of each strategy, indexed by the list of strategies from game.pure_strategies()
        '''
        strategies = game.pure_strategies(player)
        mixed_strategy = MixedStrategy.empty(game, player)
        for i, freq in enumerate(frequencies):
            mixed_strategy += strategies[i].to_mixed() * freq
        return mixed_strategy
        
    def __init__(self, mapping: dict, game: "ZeroSumGame"):
        """
        Initialize the Strategy object.
        Args:
            mapping (dict): A dictionary mapping InfoSets to np arrays of frequencies over actions.
            game (ZeroSumGame): An instance of the ZeroSumGame class representing the game.
        """
        super().__init__(mapping)
        self.game=game
    
    def sample(self, infoSet):
        """
        Return a randomly chosen action based on the frequencies.
        """
        freqs = self[infoSet]
        actions = self.game.get_actions_at_info_set(infoSet)
        return np.random.choice(actions, p=freqs)

    def __add__(self, other):
        """
        for each key, the item should be a numpy array of the same size.
        array sum each item.
        """
        assert self.keys() == other.keys()
        out = MixedStrategy(self.copy(), self.game)
        for I in self:
            freqs1 = self[I]
            freqs2 = other[I]
            assert freqs1.shape == freqs2.shape
            out[I] = freqs1 + freqs2
        return out

    def __mul__(self, scalar):
        out = MixedStrategy(self.copy(), self.game)
        for I in self:
            freqs1 = self[I]
            out[I] = freqs1 * scalar
        return out
    
class PureStrategy(dict):
    def __init__(self, mapping: dict, game: "ZeroSumGame"):
        """
        mapping: a mapping from InfoSets to action strings.
        """
        super().__init__(mapping)
        self.game = game

    def to_mixed(self):
        mixed = {}
        for I, a in self.items():
            actions = self.game.get_actions_at_info_set(I)
            index = actions.index(a)
            freqs = np.zeros(len(actions))
            freqs[index] = 1
            mixed[I] = freqs
        return MixedStrategy(mixed, self.game)
    