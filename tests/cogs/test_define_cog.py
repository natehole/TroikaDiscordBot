import discord.ext.test as dpytest
import pytest

from cogs.utils import dice


@pytest.mark.asyncio
async def test_define_weapon(bot, mocker):
    mocker.patch.object(dice, "roll_d6", return_value=4)

    dpytest.configure(bot)

    await dpytest.message("!def weapon Stinger 2 2 3 3 4 5 6")
    dpytest.verify_message("Added weapon `Stinger` damage `[2, 2, 3, 3, 4, 5, 6]` ignore_armor=False")

    await dpytest.message("!damage stinger medium")
    # FIXME: Figure out how to test the embed content here
    dpytest.verify_embed(allow_text=True)
