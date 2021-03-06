import pytest
from cogs.utils import dice
from cogs.models.weapon import Weapon


def test_init_exception():
    '''Throwing an exception'''
    with pytest.raises(ValueError):
        Weapon([0, 1, 3])


def test_init_default_values():
    '''Test how it sets optional values by default'''
    weapon = Weapon(range(7))
    assert weapon.damage == range(7)
    assert not weapon.two_handed
    assert not weapon.ignore_armor
    assert weapon.name is None
    assert weapon.style is None


def test_init_set_optional_values():
    weapon = Weapon(range(7), name="Vorpal Sword", style="melee", two_handed=True, ignore_armor=True)
    assert weapon.name == "Vorpal Sword"
    assert weapon.style == "melee"
    assert weapon.two_handed
    assert weapon.ignore_armor


def test_basic_damage_roll(mocker):
    '''A basic test of damage rolls'''
    mocker.patch.object(dice, 'roll_d6', return_value=4)
    w = Weapon(range(7))
    r = w.roll_damage()
    assert r.total == 4


def test_basic_armor_offset_roll(mocker):
    '''Armor offset should reduce damage roll to a minimum of 1'''
    mocker.patch.object(dice, 'roll_d6', return_value=2)
    w = Weapon(range(7))
    r = w.roll_damage(armor="Medium")
    assert r.total == 1


def test_ignore_armor_offset_roll(mocker):
    '''Some weapons ignore one point of the armor offset'''
    mocker.patch.object(dice, 'roll_d6', return_value=3)
    w = Weapon(range(7), ignore_armor=True)
    r = w.roll_damage(armor="Moderate")
    assert r.total == 2


def test_armor_offset_unarmored_roll(mocker):
    '''Ignoring armor should have no effect on unarmored foes'''
    mocker.patch.object(dice, 'roll_d6', return_value=2)
    w = Weapon(range(7), ignore_armor=True)
    r = w.roll_damage()
    assert r.total == 2


def test_attack_damage_mod_roll(mocker):
    '''Sometimes there are bonuses on damage rolls'''
    mocker.patch.object(dice, 'roll_d6', return_value=2)
    w = Weapon(range(7))
    r = w.roll_damage(damage_bonus=2)
    assert r.total == 4


def test_weapon_lookup_damage():
    damage = range(7)
    w = Weapon(damage)
    assert w.lookup_damage(4) == damage[3]


def test_weapon_lookup_damage_bad_index():
    w = Weapon(range(7))
    with pytest.raises(ValueError):
        w.lookup_damage(0)


def test_weapon_lookup_damage_ceiling():
    damage = range(7)
    w = Weapon(damage)
    assert w.lookup_damage(9) == damage[6]


def test_parse_explicit():
    in_weapon = {
        "damage": [1, 2, 3, 4, 5, 6, 7],
        "name": "Test Weapon",
        "style": "melee",
        "two_handed": True,
        "ignore_armor": True,
        "aliases": ["fred"]
    }

    weapon = Weapon.parse(in_weapon)
    assert weapon.damage == [1, 2, 3, 4, 5, 6, 7]
    assert weapon.name == "Test Weapon"
    assert weapon.style == "melee"
    assert weapon.two_handed
    assert weapon.ignore_armor
    assert weapon.aliases == ["fred"]


def test_parse_defaults():
    in_weapon = {
        "damage": [1, 2, 3, 4, 5, 6, 7],
        "name": "Test Weapon"
    }

    weapon = Weapon.parse(in_weapon)
    assert weapon.damage == [1, 2, 3, 4, 5, 6, 7]
    assert weapon.name == "Test Weapon"
    assert weapon.style == "melee"
    assert not weapon.two_handed
    assert not weapon.ignore_armor
    assert weapon.aliases == []
