import discord.ext.test as dpytest
import pytest

import bot
from cogs.utils import dice
from cogs.battle_cog import BattleCog
from cogs.define_cog import DefineCog


@pytest.mark.asyncio
async def test_define_weapon(mocker):
    tbot = bot.TroikaBot('!')
    mocker.patch.object(dice, "roll_d6", return_value=4)
    cog = BattleCog(tbot)
    tbot.add_cog(cog)
    cog = DefineCog(tbot)
    tbot.add_cog(cog)

    dpytest.configure(tbot)

    await dpytest.message("!def weapon Stinger 2 2 3 3 4 5 6")
    dpytest.verify_message("Added weapon `Stinger` damage `[2, 2, 3, 3, 4, 5, 6]` ignore_armor=False")

    await dpytest.message("!damage stinger medium")
    dpytest.verify_message("ROLL 1d6 (**4**) -2 [_medium armor_] = `2` DAMAGE=`2`")
