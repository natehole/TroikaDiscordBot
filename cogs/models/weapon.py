from __future__ import annotations
from typing import Dict, List
from cogs.utils import dice

ARMOR_OFFSETS: Dict[str, int] = {
    "no": 0,
    "none": 0,
    "unarmored": 0,
    "unarmoured": 0,
    "light": 1,
    "moderate": 2,
    "medium": 2,
    "heavy": 3
}

ARMOR_REGEXP_STRING: str = "(no|none|unarmored|unarmoured|light|moderate|medium|heavy)"


def normalize_armor_name(name: str) -> str:
    '''Converts armot name to lower case and removes " armor" from the back'''
    return name.lower().replace(" armor", "").replace(" armour", "")


class Weapon:
    def __init__(self, damage: List[int], name: str = None, style: str = None, two_handed: bool = False, ignore_armor: bool = False, aliases: List[str] = None):
        '''Defines a single weapon'''

        if len(damage) != 7:
            raise ValueError("You must provide a damage table of 7 elements for this weapon")

        self.damage = damage
        self.name = name
        self.style = style
        self.two_handed = two_handed
        self.ignore_armor = ignore_armor
        self.aliases = aliases or []

    def lookup_armor_offset(self, armor: str) -> int:
        if armor.isnumeric():
            return int(armor)
        else:
            return ARMOR_OFFSETS[normalize_armor_name(armor)]

    def roll_damage(self, armor: str = "No", damage_bonus: int = 0) -> dice.RollResult:
        '''Computes a damage roll, adjusting various modifiers'''
        roll = dice.roll_d6()
        roll_display = f"1d6 (**{roll}**)"

        armor_offset = self.lookup_armor_offset(armor)
        roll_display += f" -{armor_offset} [_{armor.lower()} armor_]"
        roll -= armor_offset

        if armor_offset > 0 and self.ignore_armor:
            roll_display += " +1 [_ignore armor_]"
            roll += 1

        if damage_bonus > 0:
            roll_display += f" +{damage_bonus} [_damage roll bonus_]"
            roll += damage_bonus

        if roll < 1:
            roll_display += f" = {roll} [**min value must be 1**]"
            roll = 1

        roll_display += f" = `{roll}`"

        return dice.RollResult(roll, roll_display)

    def lookup_damage(self, roll_total: int) -> int:
        '''Given a roll result, look up the damage from the weapon'''
        if roll_total < 1:
            raise ValueError("The roll must be a positive value")

        if roll_total > 7:
            roll_total = 7

        # rolls range 1-7, arrays range 0-6
        return self.damage[roll_total - 1]

    @classmethod
    def parse(cls, in_weapon: dict) -> Weapon:
        style = in_weapon.get('style', 'melee')
        ignore_armor = in_weapon.get('ignore_armor', False)
        two_handed = in_weapon.get('two_handed', False)
        aliases = in_weapon.get('aliases', [])

        return cls(
            name=in_weapon['name'],
            damage=in_weapon['damage'],
            style=style,
            ignore_armor=ignore_armor,
            two_handed=two_handed,
            aliases=aliases
        )
