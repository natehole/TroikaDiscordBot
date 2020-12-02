import pytest
from cogs.utils import dice
from cogs.models.weapon import Weapon
from cogs.models.embeds import EmbedDamage


@pytest.fixture(scope="module")
def sword():
    return Weapon(name='Sword', damage=[4, 6, 6, 6, 6, 8, 10])


def sword_damage_table(roll: int) -> str:
    if roll == 1:
        return " __**4**__ | 6 | 6 | 6 | 6 | 8 | 10 "
    elif roll == 2:
        return " 4 | __**6**__ | 6 | 6 | 6 | 8 | 10 "
    elif roll == 3:
        return " 4 | 6 | __**6**__ | 6 | 6 | 8 | 10 "
    elif roll == 4:
        return " 4 | 6 | 6 | __**6**__ | 6 | 8 | 10 "
    elif roll == 5:
        return " 4 | 6 | 6 | 6 | __**6**__ | 8 | 10 "
    elif roll == 6:
        return " 4 | 6 | 6 | 6 | 6 | __**8**__ | 10 "
    else:
        return " 4 | 6 | 6 | 6 | 6 | 8 | __**10**__ "


@pytest.fixture(scope="module")
def maul():
    return Weapon(name='Maul', damage=[1, 2, 3, 6, 12, 13, 14], ignore_armor=True)


def maul_damage_table(roll: int) -> str:
    if roll == 1:
        return " __**1**__ | 2 | 3 | 6 | 12 | 13 | 14 "
    elif roll == 2:
        return " 1 | __**2**__ | 3 | 6 | 12 | 13 | 14 "
    elif roll == 3:
        return " 1 | 2 | __**3**__ | 6 | 12 | 13 | 14 "
    elif roll == 4:
        return " 1 | 2 | 3 | __**6**__ | 12 | 13 | 14 "
    elif roll == 5:
        return " 1 | 2 | 3 | 6 | __**12**__ | 13 | 14 "
    elif roll == 6:
        return " 1 | 2 | 3 | 6 | 12 | __**13**__ | 14 "
    else:
        return " 1 | 2 | 3 | 6 | 12 | 13 | __**14**__ "


def test_damage_weapon_only(ctx, bot, sword, mocker):
    mocker.patch.object(dice, "roll_d6", return_value=2)
    embed = EmbedDamage(ctx, sword, "No", 0)

    assert embed.title == "Sword Damage (6)"
    assert embed.description == "\nRoll Breakdown:\n1d6 (2) -0 [no armor] = 2\n\nDamage Dealt:\n 4 | __**6**__ | 6 | 6 | 6 | 8 | 10 \n\n**6** damage was dealt."


@pytest.mark.parametrize("armor,offset,damage", [("light", 1, 6), ("medium", 2, 4), ("heavy", 3, 4), ("no", 0, 6)])
def test_damage_armor(ctx, bot, mocker, sword, armor, offset, damage):
    mocker.patch.object(dice, "roll_d6", return_value=3)

    floor_text = ""
    if 3 - offset < 1:
        floor_text = f"= {3-offset} [min value must be 1] "

    embed = EmbedDamage(ctx, sword, armor, 0)
    roll_result = f"1d6 (3) -{offset} [{armor} armor] {floor_text}= {max(3-offset, 1)}"

    assert embed.description == f"\nRoll Breakdown:\n{roll_result}\n\nDamage Dealt:\n{sword_damage_table(max(3-offset, 1))}\n\n**{damage}** damage was dealt."
    assert embed.title == f"Sword Damage ({damage})"


@pytest.mark.parametrize("armor,offset,damage", [("light", 1, 12), ("medium", 2, 6), ("heavy", 3, 3)])
def test_damage_ignore_armor(ctx, bot, mocker, maul, armor, offset, damage):
    mocker.patch.object(dice, "roll_d6", return_value=5)
    embed = EmbedDamage(ctx, maul, armor, 0)

    roll_result = f"1d6 (5) -{offset} [{armor} armor] +1 [ignore armor] = {5-offset+1}"
    assert embed.description == f"\nRoll Breakdown:\n{roll_result}\n\nDamage Dealt:\n{maul_damage_table(max(5-offset+1, 1))}\n\n**{damage}** damage was dealt."
    assert embed.title == f"Maul Damage ({damage})"


def test_damage_ignore_armor_no_armor(bot, ctx, maul, mocker):
    mocker.patch.object(dice, "roll_d6", return_value=5)

    embed = EmbedDamage(ctx, maul, "No", 0)

    roll_result = "1d6 (5) -0 [no armor] = 5"
    assert embed.description == f"\nRoll Breakdown:\n{roll_result}\n\nDamage Dealt:\n{maul_damage_table(5)}\n\n**12** damage was dealt."
    assert embed.title == "Maul Damage (12)"


def test_damage_bonus(ctx, bot, maul, mocker):
    mocker.patch.object(dice, "roll_d6", return_value=3)

    embed = EmbedDamage(ctx, maul, "No", 2)
    roll_result = "1d6 (3) -0 [no armor] +2 [damage roll bonus] = 5"
    assert embed.description == f"\nRoll Breakdown:\n{roll_result}\n\nDamage Dealt:\n{maul_damage_table(5)}\n\n**12** damage was dealt."
    assert embed.title == "Maul Damage (12)"
