from typing import Callable, List, Any, Dict, Optional, Tuple
import numpy as np

class SequentialGame:
    def __init__(
        self,
        actions: Callable[[Tuple[Any, ...]], List[Any]],
        player: Callable[[Tuple[Any, ...]], int],
        types: Callable[[], Tuple[Any, ...]],
        terminal: Callable[[Tuple[Any, ...]], bool],
        payoff: Callable[[Tuple[Any, ...], Any, Any], float]
    ):
        self.actions = actions
        self.player = player
        self.types = types
        self.terminal = terminal
        self.payoff = payoff
    
    def get_actions(self, history):
        # get legal actions at this history
        if self.is_terminal(history):
            # TODO: raise error instead?
           return []
        return self.actions(history)
    
    def get_player(self, history):
        # get the current player at this history
        if self.is_terminal(history):
            # TODO: raise error instead?
           return []
        return self.player(history)
    
    def get_types(self):
        return self.types()
    
    def is_terminal(self, history):
        return self.terminal(history)
    
    def get_payoff(self, history, types):
        assert self.is_terminal(history), "Cannot get payoff for non-terminal state"    
        return self.payoff(history, *types)

    def get_instance(self, types: Optional[Tuple[Any, ...]] = None, history: Optional[Tuple[Any, ...]] = None):
        if types is None:
            types = self.get_types()
        if history is None:
            history = ()
        return SequentialGameState(self, types=types, history=history)

    def __repr__(self):
        return f"SequentialGame(actions={self.actions.__name__ if hasattr(self.actions, '__name__') else 'λ'})"


class SequentialGameState:
    def __init__(
        self,
        game: SequentialGame,
        types: Tuple[Any, ...],
        history: Optional[Tuple[Any, ...]] = None
    ):
        self.game = game
        self.types = types
        self.history = ()
        if history:
            self.play_action_sequence(history, inplace=True)

    def play_action(self, action: Any, inplace: bool = False) -> Optional['SequentialGameState']:
        legal_actions = self.game.get_actions(self.history)
        assert action in legal_actions, f"'{action}' is not a legal action. Legal actions: {legal_actions}"

        if inplace:
            self.history = self.history + (action,)
            return None
        else:
            new_instance = SequentialGameState(self.game, self.types, self.history)
            new_instance.history = new_instance.history + (action,)
            return new_instance

    def play_action_sequence(self, actions: Tuple[Any, ...], inplace: bool = False) -> Optional['SequentialGameState']:
        if inplace:
            for action in actions:
                self.play_action(action, inplace=True)
            return None
        else:
            new_instance = SequentialGameState(self.game, self.types, self.history)
            for action in actions:
                new_instance.play_action(action, inplace=True)
            return new_instance
        
    def get_history(self):
        return self.history

    def is_terminal(self) -> bool:
        return self.game.is_terminal(self.history)

    def get_actions(self) -> List[Any]:
        return self.game.get_actions(self.history)
    
    def get_player(self) -> List[Any]:
        return self.game.get_player(self.history)

    def get_payoff(self) -> float:
        return self.game.get_payoff(self.history, self.types)

    def copy(self) -> 'SequentialGameState':
        return SequentialGameState(self.game, self.types, self.history)

    def __repr__(self):
        terminal_str = " [TERMINAL]" if self.is_terminal() else ""
        return f"SequentialGameInstance(types={self.types}, history={self.history}{terminal_str})"
