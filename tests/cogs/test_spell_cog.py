import discord.ext.test as dpytest
import pytest

from cogs.utils import dice


@pytest.mark.asyncio
async def test_spell_cog(bot, mocker):
    dpytest.configure(bot)

    await dpytest.message("!oops")
    dpytest.verify_embed(allow_text=True)

    await dpytest.message("!spell darkness")
    dpytest.verify_embed(allow_text=True)

    mocker.patch.object(dice, 'roll_2d6', return_value=(1, 2, 3))
    await dpytest.message("!cast 7")
    dpytest.verify_embed(allow_text=True)

    mocker.patch.object(dice, 'roll_2d6', return_value=(5, 5, 10))
    await dpytest.message("!cast 7 read entrails")
    dpytest.verify_embed(allow_text=True)

    mocker.patch.object(dice, "roll_2d6", return_value=(1, 1, 2))
    await dpytest.message("!cast 1")
    dpytest.verify_embed(allow_text=True)

    mocker.patch.object(dice, "roll_2d6", return_value=(6, 6, 12))
    await dpytest.message("!cast 7")
    dpytest.verify_embed(allow_text=True)
