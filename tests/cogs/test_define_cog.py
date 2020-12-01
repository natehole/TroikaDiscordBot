import discord.ext.test as dpytest
import pytest

from bot import TroikaBot
from cogs.utils import dice
from cogs.library_cog import LibraryCog
from cogs.battle_cog import BattleCog
from cogs.define_cog import DefineCog

@pytest.fixture(scope="function")
def bot():
   bot = TroikaBot('!')
   bot.add_cog(LibraryCog(bot))
   bot.add_cog(BattleCog(bot))
   bot.add_cog(DefineCog(bot))
   return bot


@pytest.mark.asyncio
@pytest.mark.skip
async def test_define_weapon(bot, mocker):
    mocker.patch.object(dice, "roll_d6", return_value=4)

    dpytest.configure(bot)

    await dpytest.message("!def weapon Stinger 2 2 3 3 4 5 6")
    dpytest.verify_message("Added weapon `Stinger` damage `[2, 2, 3, 3, 4, 5, 6]` ignore_armor=False")

    await dpytest.message("!damage stinger medium")
    dpytest.verify_message("ROLL 1d6 (**4**) -2 [_medium armor_] = `2` DAMAGE=`2`")
