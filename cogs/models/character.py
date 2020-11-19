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

    def __str__(self) -> str:
        return interpolate_dice(self.name)


@dataclass
class ItemChoice:
    choices: List[Item]

    def __str__(self) -> str:
        choices = "\n".join([f"  - {c.name}" for c in self.choices])
        return f"_One of:_\n{choices}\n"

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

    def __str__(self) -> str:
        return f"{self.rank} {self.name}"

    @classmethod
    def parse(cls, skill: str) -> Skill:
        r = re.match(r'([0-9]+) (.+)', skill)
        if not r:
            raise ValueError(f"Unable to parse skill: {skill}")

        return cls(rank=int(r.group(1)), name=r.group(2))


class RandomSpellPicker:
    def __init__(self, compendium: Compendium, spells: List[str]):
        spells = [s.split(' ', 1)[1] for s in spells] # Go from 1 Jolt -> Jolt
        self.compendium = compendium
        self.available_spells: List[str] = list(compendium.spells.keys())
        self.available_spells = [s for s in self.available_spells if s not in spells]
        random.shuffle(self.available_spells)

    def fetch_spell(self, spell_name: str) -> Spell:
        if spell_name == 'Random':
            spell_name = self.available_spells.pop()
        return self.compendium.spells[spell_name]


@dataclass
class SpellSkill(Skill):
    spell: Spell

    def __str__(self) -> str:
        return f"{self.rank} {self.name} ({self.spell.cost})"

    @classmethod
    def parse(cls, text: str, spell_picker: SpellPicker) -> SpellSkill:
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

    def __str__(self):
        items = "\n".join([f"- {i}" for i in self.items])
        skills = "\n".join([f"- {s}" for s in self.skills])

        output = f"""SKILL d3 ({self.skill-3})+3 = `{self.skill}`
STAMINA 2d6 ({self.stamina-12})+12 = `{self.stamina}`
LUCK d6 ({self.luck-6})+6 = `{self.luck}`
BACKGROUND d66 = `{self.background.roll}`

**{self.background.roll}** {self.background.name}
_{self.background.description}_
"""
        if len(self.background.special) > 0:
            special = "\n".join([f"- {s}" for s in self.background.special])
            output += f"""
SPECIAL:
{special}
"""
        output += f"""
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
