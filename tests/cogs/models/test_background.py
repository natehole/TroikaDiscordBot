import pytest
from cogs.models.background import Background, Skill, Item, ItemChoice, SpellSkill
import yaml

BACKGROUND_YAML = """
id: 65
name: Yongardy Lawyer
desc: >-
  Down in Yongardy they do things differently. They respect the Law. Every
  day there is a queue outside the courts to get a seat to see the latest up
  and coming barrister defend their case with a metre of steel. The people
  follow the careers of their favourite solicitors, watch all their cases,
  collect their portraits, and sneak into the court after hours to dab the
  patches of blood on white handkerchiefs.

  In Yongardy, they love the Law.
items:
  - - Rapier (damage as Sword) and Puffy Shirt
    - Sjambok (damage as Club) and Lots Of Scars
    - Longsword and Heavy Armour
    - Hammer and Gargantuan Shield
  - Manual on Yongardy Law
  - Barrister's Wig
skills:
  - 4 Fighting in your chosen Weapon
  - 2 Etiquette
  - 1 Healing
"""

def test_background_parse():
    parsed = yaml.safe_load(BACKGROUND_YAML)
    background = Background.parse(parsed)

    assert background.roll == 65
    assert background.name == "Yongardy Lawyer"
    assert background.description is not None

    assert background.items
    assert len(background.items) == 8
    item1 = background.items[0]
    assert isinstance(item1, ItemChoice)
    assert len(item1.choices) == 4
    assert background.items[1] == Item('Manual on Yongardy Law')
    assert background.items[7] == Item('6 Provisions')

    assert background.skills
    assert len(background.skills) == 3
    assert background.skills[0].rank == 4
    assert background.skills[0].name == 'Fighting in your chosen Weapon'

    assert background.spells == []
