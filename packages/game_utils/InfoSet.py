from dataclasses import dataclass


@dataclass(frozen=True)
class InfoSet:
    type: str
    history: tuple
    