from __future__ import annotations
from typing import List, Union
from dataclasses import dataclass, field
import re
import random

from cogs.utils import dice
from cogs.utils.dice import interpolate_dice
from cogs.models.spell import Spell
from cogs.models.background import Background
from cogs.models.compendium import Compendium


@dataclass
class Item:
    name: str

    @classmethod
    def parse(cls, name: str) -> Item:
        return cls(name=interpolate_dice(name))


@dataclass
class ItemChoice:
    choices: List[Item]

    @classmethod
    def parse(cls, yaml: Union[str, dict]) -> Union[Item, ItemChoice]:
        if isinstance(yaml, str):
            return Item.parse(yaml)
        elif isinstance(yaml, list):
            items = [Item.parse(item) for item in yaml]
            return cls(choices=items)
        else:
            raise ValueError("For items, only a string or an array of strings is accepted")


@dataclass
class Skill:
    name: str
    rank: int

    @classmethod
    def parse(cls, skill: str) -> Skill:
        r = re.match(r'(-?[0-9]+) (.+)', skill)
        if not r:
            raise ValueError(f"Unable to parse skill: {skill}")

        return cls(rank=int(r.group(1)), name=r.group(2))


class RandomSpellPicker:
    def __init__(self, compendium: Compendium, spells: List[str]):
        spells = [s.split(' ', 1)[1] for s in spells] # Go from 1 Jolt -> Jolt
        self.compendium = compendium
        self.available_spells: List[str] = list([s.name for s in compendium.spells])
        random.shuffle(self.available_spells)

    def fetch_spell(self, spell_name: str) -> Spell:
        if spell_name == 'Random':
            spell_name = self.available_spells.pop()
        spell = self.compendium.lookup_spell(spell_name)
        if not spell:
            raise ValueError(f"Unable to find spell `{spell_name}` in compendium `{self.compendium.key}` (or parent compendium). Check its spelling?")

        return spell


@dataclass
class SpellSkill(Skill):
    spell: Spell

    def __str__(self) -> str:
        return f"{self.rank} {self.name} ({self.spell.cost})"

    @classmethod
    def parse(cls, text: str, spell_picker: RandomSpellPicker) -> SpellSkill:
        skill = Skill.parse(text)
        spell = spell_picker.fetch_spell(skill.name)
        return cls(name=spell.name, rank=skill.rank, spell=spell)



@dataclass
class Character:
    """
    Represents a playable character (right now just using to generate characters
    and not save state)

    """
    skill: int
    stamina: int
    luck: int
    background: Background
    compendium: Compendium
    items: List[Item]
    skills: List[Skill]
    spells: List[SpellSkill]

    @classmethod
    def generate(cls, compendium: Compendium, background: Background) -> Character:
        skill_roll = dice.roll_d3()
        _, _, stamina_roll = dice.roll_2d6()
        luck_roll = dice.roll_d6()

        skills: List[Skill] = [Skill.parse(s) for s in background.skills]
        items: List[Union[Item, ItemChoice]] = [ItemChoice.parse(i) for i in background.items]

        if background.base_items:
            items += [Item.parse(i) for i in background.base_items]
        elif compendium.base_items:
            items += [Item.parse(i) for i in compendium.base_items]

        spell_picker = RandomSpellPicker(compendium, background.spells)
        spells: List[Spell] = [SpellSkill.parse(s, spell_picker) for s in background.spells]

        return cls(
            skill=skill_roll + 3,
            stamina=stamina_roll + 12,
            luck=luck_roll + 6,
            background=background,
            compendium=compendium,
            items=items,
            skills=skills,
            spells=spells
        )

    @property
    def description(self) -> str:
        return self.background.description

    @property
    def background_name(self) -> str:
        return self.background.name

    @property
    def background_roll(self) -> int:
        return self.background.roll

    @property
    def specials(self) -> List[str]:
        return self.background.special
