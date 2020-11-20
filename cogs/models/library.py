from __future__ import annotations
from typing import List, Union, Optional

from cogs.models.weapon import Weapon
from cogs.models.background import Background
from cogs.models.compendium_link import CompendiumLink
from cogs.models.compendium import Compendium


class Library:
    def __init__(self):
        self.compendiums: Dict[str, Compendium] = {}

    def load_compendium(self, path: str) -> None:
        compendium = Compendium.load(path)

        # Resolve inherits
        if compendium.inherits:
            parent_compendium = self.find_compendium(compendium.inherits)
            if not parent_compendium:
                raise ValueError(f"This compendium (`{compendium.key}`) inherits from a parent compendium (`{compendium.inherits}`) that must be loaded first.")
            compendium.parent_compendium = CompendiumLink(self.compendiums, compendium.inherits)

        self.validate_compendium(compendium)
        self.compendiums[compendium.key] = compendium

    def validate_compendium(self, compendium: Compendium):
        pass

    def find_compendium(self, key: str = 'base') -> Optional[Compendium]:
        return self.compendiums.get(key, None)

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
