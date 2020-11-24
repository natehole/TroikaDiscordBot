from __future__ import annotations
from typing import List, Union, Optional
from dataclasses import dataclass, field

from cogs.utils.dice import interpolate_dice


@dataclass
class Background:
    roll: int
    name: str
    description: str
    skills: List[str]
    items: List[Union[str, List[str]]]
    special: List[str] = field(default_factory=list)
    spells: List[str] = field(default_factory=list)
    base_items: Optional[List[str]] = None

    @classmethod
    def parse(cls, yaml: dict):
        skills = yaml.get('skills', [])
        items = yaml.get('items', [])
        spells = yaml.get('spells', [])
        base_items = yaml.get('base_items', None)

        special = []
        if 'special' in yaml:
            if isinstance(yaml['special'], str):
                special = [yaml['special']]
            elif isinstance(yaml['special'], list):
                special = yaml['special']
            else:
                raise ValueError("Special must be a string or a list")

        return cls(roll=yaml['id'], name=yaml['name'], description=yaml['desc'], skills=skills, items=items, spells=spells, special=special, base_items=base_items)
