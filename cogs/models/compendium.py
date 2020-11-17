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


@dataclass
class Compendium:
    '''Represents a single data file loaded from the data directory'''
    title: str
    key: str
    url: Optional[str] = None
    author: Optional[str] = None
    backgrounds: Dict[int, Background] = field(default_factory=dict)
    weapons: List[Weapon] = field(default_factory=list)
    spells: List[Spell] = field(default_factory=list)
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

        spells: List[Spell] = []
        if 'spells' in infile:
            for in_spell in infile['spells']:
                spell = Spell.parse(in_spell)
                spells.append(spell)

        return cls(key=key, title=title, url=url, author=author, backgrounds=backgrounds, weapons=weapons, spells=spells)

    def lookup_weapon(self, name: str) -> Union[Weapon, None]:
        '''Looks up a weapon by name'''
        pass

    def lookup_background(self, roll: int) -> Union[Background, None]:
        '''Looks up a background by ID or returns None if not found'''
        return self.backgrounds.get(roll, None)
