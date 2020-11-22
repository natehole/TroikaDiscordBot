from __future__ import annotations
from dataclasses import dataclass, field


@dataclass
class Spell:
    name: str
    cost: str
    description: str

    @classmethod
    def parse(cls, yaml: dict) -> Spell:
        return cls(name=yaml['name'], cost=yaml['cost'], description=yaml['desc'])
