from __future__ import annotations
import os
from urllib.parse import urlparse
from urllib.request import urlopen
from typing import List, Union, Optional, Dict
import yaml

from cogs.models.spell import Spell
from cogs.models.background import Background
from cogs.models.weapon import Weapon
from cogs.models.compendium_link import CompendiumLink

def normalize(name: str) -> str:
    return name.strip().lower().replace(" ", "-")

class Compendium:
    '''Represents a single data file loaded from the data directory'''
    def __init__(self, key: str, title: str, url: str = None, author: str = None, inherits: str = None):
        self.title = title
        self.key = key
        self.url = url
        self.author = author
        self.inherits = inherits
        self.parent_compendium: Optional[CompendiumLink] = None
        self._backgrounds: Dict[int, Background] = {}
        self._weapons: Dict[str, Weapon] = {}
        self._spells: Dict[str, Spell] = {}
        self._base_items: List[str] = []

    def add_background(self, background: Background):
        # FIXME: Do background validation here?
        self._backgrounds[background.roll] = background

    def add_weapon(self, weapon: Weapon):
        self._weapons[normalize(weapon.name)] = Weapon
        # Add aliases here

    def add_spell(self, spell: Spell):
        self._spells[normalize(spell.name)] = spell

    def add_base_item(self, item: str):
        self._base_items.append(item)

    def link_parent(self, parent: CompendiumLink):
        self.parent_compendium = parent

    @classmethod
    def load(cls, path: str) -> Compendium:
        yaml_data = None

        config_uri_parsed = urlparse(path)
        if config_uri_parsed.scheme in ['https', 'http']:
            url = urlopen(path)
            yaml_data = url.read()
        else:
            if not os.path.exists(path):
                path = os.path.join(os.path.dirname(__file__), '..', '..', 'data', f"{path}.yaml")

            with open(path, 'r') as file_data:
                yaml_data = file_data.read()

        infile = yaml.safe_load(yaml_data)

        key = infile['key']
        title = infile['title']
        url = infile.get('url', None)
        author = infile.get('author', None)
        inherits = infile.get('inherits', None)

        compendium = cls(key, title, url, author, inherits)
        if 'backgrounds' in infile:
            for in_bg in infile['backgrounds']:
                background = Background.parse(in_bg)
                compendium.add_background(background)

        if 'weapons' in infile:
            for in_weapon in infile['weapons']:
                weapon = Weapon.parse(in_weapon)
                compendium.add_weapon(weapon)

        if 'spells' in infile:
            for in_spell in infile['spells']:
                spell = Spell.parse(in_spell)
                compendium.add_spell(spell)

        if 'base_items' in infile:
            for base_item in infile['base_items']:
                compendium.add_base_item(base_item)

        return compendium

    def lookup_weapon(self, name: str) -> Union[Weapon, None]:
        '''Looks up a weapon by name'''
        weapon = self._weapons.get(normalize(name), None)
        if weapon:
            return weapon

        if self.parent_compendium:
            return self.parent_compendium.ref.lookup_weapon(name)

        return None

    def lookup_background(self, roll: int) -> Union[Background, None]:
        '''Looks up a background by ID or returns None if not found'''
        bg = self._backgrounds.get(roll, None)
        if bg:
            return bg

        # FIXME?
        if self.parent_compendium:
            return self.parent_compendium.ref.lookup_background(roll)

        return None

    def lookup_spell(self, name: str) -> Union[Spell, None]:
        spell = self.lookup_own_spell(name)
        if spell:
            return spell

        if self.parent_compendium:
            return self.parent_compendium.ref.lookup_spell(name)

        return None

    def lookup_own_spell(self, name: str) -> Union[Spell, None]:
        return self._spells.get(normalize(name), None)

    @property
    def base_items(self) -> List[str]:
        if len(self._base_items) > 0:
            return self._base_items

        if self.parent_compendium:
            return self.parent_compendium.ref.base_items

        return []

    @property
    def spells(self) -> List[Spell]:
        spells = list(self._spells.values())

        if self.parent_compendium:
            spells += self.parent_compendium.ref.spells

        return spells
