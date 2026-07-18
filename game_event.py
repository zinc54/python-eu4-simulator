from dataclasses import dataclass


@dataclass
class GameEvent:
    month: int
    actor_name: str
    message: str
    category: str
