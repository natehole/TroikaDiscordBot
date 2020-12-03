from cogs.utils import dice, oops
from cogs.models.embeds import EmbedSpell
from cogs.models.spell import Spell


def test_with_spell_name(ctx):
    spell = Spell(name="Zap", cost='3', description="The wizard makes things go boom!")
    embed = EmbedSpell(ctx, spell)

    assert embed.description == spell.description
    assert embed.title == f"{spell.name} ({spell.cost})"


def test_with_spell_cast(ctx, mocker):
    mocker.patch.object(dice, 'roll_2d6', return_value=(1, 3, 4))

    embed = EmbedSpell(ctx, None, dice.roll_under(7))
    assert embed.title == "Spell Casting"
    assert len(embed.fields) == 1

    assert embed.fields[0].name == "Outcome"
    assert embed.fields[0].value == "**SUCCESS** 2d6(1+3) = `4` ≤ `7`"
    assert not embed.fields[0].inline


def test_with_spell_name_and_cast(ctx, mocker):
    spell = Spell(name="Zap", cost='3', description="The wizard makes things go boom!")
    mocker.patch.object(dice, 'roll_2d6', return_value=(6, 3, 9))

    embed = EmbedSpell(ctx, spell, dice.roll_under(7))

    assert embed.description == spell.description
    assert embed.title == f"{spell.name} ({spell.cost})"
    assert len(embed.fields) == 1

    assert embed.fields[0].name == "Outcome"
    assert embed.fields[0].value == "**FAILURE** 2d6(6+3) = `9` > `7`"
    assert not embed.fields[0].inline


def test_with_oops(ctx, mocker):
    spell = Spell(name="Zap", cost='3', description="The wizard makes things go boom!")
    mocker.patch.object(dice, 'roll_2d6', return_value=(6, 6, 12))
    mocker.patch.object(oops, 'roll_oops', return_value=(61, "A calm and healthy pig appears in place of the Spell."))

    embed = EmbedSpell(ctx, spell, dice.roll_under(7))

    assert embed.description == spell.description
    assert embed.title == f"{spell.name} ({spell.cost})"
    assert len(embed.fields) == 2

    assert embed.fields[0].name == "Outcome"
    assert embed.fields[0].value == "**CATASTROPHIC FAILURE** 2d6(6+6)"
    assert not embed.fields[0].inline

    assert embed.fields[1].name == "Ooops! (61)"
    assert embed.fields[1].value == "A calm and healthy pig appears in place of the Spell."
