from dataclasses import dataclass


@dataclass
class EnemyData:
    name: str = None
    max_hp: int = None
    strength: int = None
    potions: int = None
