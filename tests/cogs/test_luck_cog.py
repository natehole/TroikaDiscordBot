import discord.ext.test as dpytest
import pytest

from bot import TroikaBot
from cogs.utils import dice
from cogs.library_cog import LibraryCog
from cogs.luck_cog import LuckCog


@pytest.fixture(scope="function")
def bot():
   bot = TroikaBot('!')
   bot.add_cog(LibraryCog(bot))
   bot.add_cog(LuckCog(bot))
   return bot


@pytest.mark.asyncio
async def test_luck(bot, mocker):
    mocker.patch.object(dice, "roll_2d6", return_value=(3, 4, 7))

    dpytest.configure(bot)

    await dpytest.message("!luck 8")
    dpytest.verify_message("**SUCCESS** 2d6(3+4) = `7` ≤ `8`")

    await dpytest.message("!luck 6")
    dpytest.verify_message("**FAILURE** 2d6(3+4) = `7` > `6`")
