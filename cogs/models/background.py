from __future__ import annotations
from typing import List, Union
from dataclasses import dataclass, field
import re

from cogs.utils.dice import interpolate_dice


STARTING_ITEMS = [
    '2d6 Silver Pence',
    'Knife',
    'Lantern & flask of oil',
    'Rucksack',
    '6 Provisions'
]


@dataclass
class Skill:
    name: str
    rank: int

    def __str__(self) -> str:
        return f"{self.rank} {self.name}"

    @classmethod
    def parse(cls, skill: str) -> Skill:
        r = re.match(r'([0-9]+) (.+)', skill)
        if not r:
            raise ValueError(f"Unable to parse skill: {skill}")

        return cls(rank=int(r.group(1)), name=r.group(2))


@dataclass
class SpellSkill(Skill):
    pass


@dataclass
class Item:
    name: str

    def __str__(self) -> str:
        return interpolate_dice(self.name)


@dataclass
class ItemChoice:
    choices: List[Item]

    def __str__(self) -> str:
        choices = "\n".join([f"  - {interpolate_dice(c.name)}" for c in self.choices])
        return f"_One of:_\n{choices}\n"

    @classmethod
    def parse(cls, yaml: Union[str, dict]) -> Union[Item, ItemChoice]:
        if isinstance(yaml, str):
            return Item(name=yaml)
        elif isinstance(yaml, list):
            items = [Item(name=item) for item in yaml]
            return cls(choices=items)
        else:
            raise ValueError("For items, only a string or an array of strings is accepted")

@dataclass
class Background:
    roll: int
    name: str
    description: str
    skills: List[Skill]
    items: List[Union[Item, ItemChoice]]
    spells: List[SpellSkill] = field(default_factory=list)

    def __str__(self):
        items = "\n".join([f"- {i}" for i in self.items])
        skills = "\n".join([f"- {s}" for s in self.skills])

        output = f"""**{self.roll}** {self.name}
_{self.description}_

ITEMS:
{items}

SKILLS:
{skills}
"""

        if len(self.spells) > 0:
            spells = "\n".join([f"- {s}" for s in self.spells])
            output += f"""
SPELLS:
{spells}
"""
        return output

    @classmethod
    def parse(cls, yaml: dict):
        skills: List[Skill] = []
        if 'skills' in yaml:
            skills += [Skill.parse(s) for s in yaml['skills']]

        items: List[Item] = []
        if 'items' in yaml:
            items += [ItemChoice.parse(i) for i in yaml['items']]

        for i in STARTING_ITEMS:
            items.append(Item(name=i))

        spells: List[SpellSkill] = []
        if 'spells' in yaml:
            spells += [SpellSkill.parse(i) for i in yaml['spells']]

        return cls(roll=yaml['id'], name=yaml['name'], description=yaml['desc'], skills=skills, items=items, spells=spells)
