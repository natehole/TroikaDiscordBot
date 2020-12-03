from __future__ import annotations
from typing import List, Union
from dataclasses import dataclass, field


@dataclass
class Background:
    roll: int
    name: str
    description: str
    skills: List[str]
    items: List[Union[str, List[str]]]
    special: List[str] = field(default_factory=list)
    spells: List[str] = field(default_factory=list)
    has_base_items: bool = True

    @classmethod
    def parse(cls, yaml: dict):
        skills = yaml.get('skills', [])
        items = yaml.get('items', [])
        spells = yaml.get('spells', [])
        has_base_items = yaml.get('base_items', True)

        special = []
        if 'special' in yaml:
            if isinstance(yaml['special'], str):
                special = [yaml['special']]
            elif isinstance(yaml['special'], list):
                special = yaml['special']
            else:
                raise ValueError("Special must be a string or a list")

        return cls(roll=yaml['id'], name=yaml['name'], description=yaml['desc'], skills=skills, items=items, spells=spells, special=special, has_base_items=has_base_items)
