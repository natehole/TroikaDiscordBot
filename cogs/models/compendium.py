from __future__ import annotations
import os
from urllib.parse import urlparse
from urllib.request import urlopen
from typing import List, Union, Optional, Dict
from dataclasses import dataclass, field
import yaml

from cogs.models.spell import Spell
from cogs.models.background import Background
from cogs.models.weapon import Weapon
from cogs.models.compendium_link import CompendiumLink

@dataclass
class Compendium:
    '''Represents a single data file loaded from the data directory'''
    title: str
    key: str
    url: Optional[str] = None
    author: Optional[str] = None
    backgrounds: Dict[int, Background] = field(default_factory=dict)
    weapons: List[Weapon] = field(default_factory=list)
    spells: Dict[str, Spell] = field(default_factory=dict)
    base_items: List[str] = field(default_factory=list)
    inherits: Optional[str] = None
    parent_compendium: Optional[CompendiumLink] = None
    # creatures: List[Creature] = field(default_factory=list)
    # tables: List[RollTable] = field(default_factory=list)

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

        backgrounds: Dict[int, Background] = {}
        if 'backgrounds' in infile:
            for in_bg in infile['backgrounds']:
                background = Background.parse(in_bg)
                backgrounds[background.roll] = background

        weapons: List[Weapon] = []
        if 'weapons' in infile:
            for in_weapon in infile['weapons']:
                weapon = Weapon.parse(in_weapon)
                weapons.append(weapon)

        spells: Dict[str, Spell] = {}
        if 'spells' in infile:
            for in_spell in infile['spells']:
                spell = Spell.parse(in_spell)
                spells[spell.name] = spell

        base_items = infile.get('base_items', [])

        return cls(key=key, title=title, url=url, author=author, backgrounds=backgrounds, weapons=weapons, spells=spells, base_items=base_items, inherits=inherits)

    def lookup_weapon(self, name: str) -> Union[Weapon, None]:
        '''Looks up a weapon by name'''
        pass

    def lookup_background(self, roll: int) -> Union[Background, None]:
        '''Looks up a background by ID or returns None if not found'''
        bg = self.backgrounds.get(roll, None)
        if bg:
            return bg

        # FIXME?
        if self.parent_compendium:
            return self.parent_compendium.ref.lookup_background(roll)

        return None

    def lookup_spell(self, name: str) -> Union[Spell, None]:
        spell = self.spells.get(name, None)
        if spell:
            return spell

        if self.parent_compendium:
            return self.parent_compendium.ref.lookup_spell(name)

    def list_base_items(self) -> List[str]:
        if len(self.base_items) > 0:
            return self.base_items

        if self.parent_compendium:
            return self.parent_compendium.ref.list_base_items()

        return []

    def list_spells(self) -> List[Spell]:
        spells = list(self.spells.values())

        if self.parent_compendium:
            spells += self.parent_compendium.ref.list_spells()

        return spells
