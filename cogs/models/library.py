from __future__ import annotations
from typing import List, Union, Optional
from dataclasses import dataclass, field

from cogs.models.weapon import Weapon
from cogs.models.background import Background
from cogs.models.compendium import Compendium

@dataclass
class Library:
    compendiums: List[Compendium] = field(default_factory=list)

    def load_compendium(self, path: str) -> None:
        self.compendiums.append(Compendium.load(path))

    def find_compendium(self, key: str = 'base') -> Optional[Compendium]:
        for c in self.compendiums:
            if c.key == key:
                return c
        return None

    def lookup_weapon(self, name: str) -> Optional[Weapon]:
        pass

    def lookup_background(self, roll: int, key: str = None) -> List[Background]:
        backgrounds: List[Background] = []

        for comp in self.compendiums:
            if key is None or comp.key == key:
                b = comp.lookup_background(roll)
                if b:
                    backgrounds.append(b)

        return backgrounds
