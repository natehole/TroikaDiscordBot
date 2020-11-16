from typing import List, Union
from dataclasses import dataclass, field
import re

from cogs.utils.dice import interpolate_dice


STARTING_ITEMS = [
    '2d6 Silver Pence',
    'Knife',
    'Lantern & flask of oil'
    'Rucksack',
    '6 Provisions'
]


@dataclass
class Skill:
    name: str
    rank: int

    def __str__(self) -> str:
        return f"- {self.rank} {self.name}"

    @classmethod
    def parse(cls, skill: str):
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

    def __str__(self):
        return f"- {interpolate_dice(self.name)}"


@dataclass
class ItemChoice:
    choices: List[Item]

    def __str__(self):
        choices = "\n".join([f"  - {c.name}" for c in self.choices])
        return f"- _One of:_\n{choices}\n"

    @classmethod
    def parse(cls, key: str, yaml: Union[str, dict]):
        if isinstance(yaml, str):
            return Item(name=yaml)
        else:
            if not yaml['choice']:
                raise ValueError("For items, only a string or a top-level choice key is accepted")
            items = [Item(name=item) for item in yaml['choice']]
            return ItemChoice(choices=items)


@dataclass
class Background:
    id: int
    source_key: str
    name: str
    description: str
    skills: List[Skill]
    items: List[Item]
    spells: List[SpellSkill] = field(default_factory=list)

    @classmethod
    def parse(cls, key: str, yaml: dict):
        skills: List[Skill] = []
        if 'skills' in yaml:
            skills.append([Skill.parse(s) for s in yaml['skills']])

        items: List[Item] = []
        if 'items' in yaml:
            items.append([ItemChoice.parse(key, i) for i in yaml['items']])
        items.append([Item(name=i) for i in STARTING_ITEMS])

        spells: List[SpellSkill] = []
        if 'spells' in yaml:
            spells.append([SpellSkill.parse(i) for i in yaml['spells']])

        return cls(id=yaml['id'], source_key=key, name=yaml['name'], description=yaml['desc'], skills=skills, items=items, spells=spells)
