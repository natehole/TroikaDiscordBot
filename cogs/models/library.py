from __future__ import annotations
from typing import Dict, List, Union, Optional, Tuple
import random

from cogs.models.spell import Spell
from cogs.models.weapon import Weapon
from cogs.models.background import Background
from cogs.models.compendium_link import CompendiumLink
from cogs.models.compendium import Compendium, normalize


class Library:
    def __init__(self):
        self.compendiums: Dict[str, Compendium] = {}
        self.temp_weapons: Dict[str, Weapon] = {}

    def load_compendium(self, path: str) -> None:
        compendium = Compendium.load(path)

        # Resolve inherits
        if compendium.inherits:
            parent_compendium = self.find_compendium(compendium.inherits)
            if not parent_compendium:
                raise ValueError(f"This compendium (`{compendium.key}`) inherits from a parent compendium (`{compendium.inherits}`) that must be loaded first.")
            compendium.link_parent(CompendiumLink(self.compendiums, compendium.inherits))

        self.validate_compendium(compendium)
        self.compendiums[compendium.key] = compendium

    def validate_compendium(self, compendium: Compendium):
        """We should probably have some code to validate compendiums"""
        pass

    def find_compendium(self, key: str = 'base') -> Optional[Compendium]:
        return self.compendiums.get(key, None)

    def lookup_background(self, roll: int, key: str = None) -> List[Background]:
        backgrounds: List[Background] = []

        for comp in self.compendiums.values():
            if key is None or comp.key == key:
                b = comp.lookup_background(roll)
                if b:
                    backgrounds.append(b)

        return backgrounds

    def lookup_spell(self, spell_name: str) -> Optional[Spell]:
        for comp in self.compendiums.values():
            spell = comp.lookup_own_spell(spell_name)
            if spell:
                return spell

        return None

    @property
    def all_spells(self) -> List[Spell]:
        spells: List[Spell] = []
        for comp in self.compendiums.values():
            spells += comp.own_spells

        return spells

    def random_spell(self) -> Spell:
        return random.choice(self.all_spells)

    def lookup_weapon(self, weapon_name: str) -> Optional[Weapon]:
        normalized = normalize(weapon_name)
        if normalized in self.temp_weapons:
            return self.temp_weapons[normalized]

        for comp in self.compendiums.values():
            weapon = comp.lookup_weapon(weapon_name)
            if weapon:
                return weapon

        return None

    def add_temp_weapon(self, weapon: Weapon):
        self.temp_weapons[normalize(weapon.name)] = weapon
