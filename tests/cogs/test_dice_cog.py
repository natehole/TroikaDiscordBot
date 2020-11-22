import discord.ext.test as dpytest
import pytest

from bot import TroikaBot
from cogs.utils import dice
from cogs.library_cog import LibraryCog
from cogs.dice_cog import DiceCog

@pytest.fixture(scope="function")
def bot():
   bot = TroikaBot('!')
   bot.add_cog(LibraryCog(bot))
   bot.add_cog(DiceCog(bot))
   return bot

@pytest.mark.asyncio
async def test_roll_d2(bot, mocker):
    mocker.patch.object(dice, "roll_d2", return_value=2)

    dpytest.configure(bot)

    await dpytest.message("!roll d2")
    dpytest.verify_message("d2 (2) = `2`")

    await dpytest.message("!roll 1d2")
    dpytest.verify_message("d2 (2) = `2`")

    await dpytest.message("!roll 1d2+6")
    dpytest.verify_message("d2 (2)+6 = `8`")


@pytest.mark.asyncio
async def test_roll_d3(bot, mocker):
    mocker.patch.object(dice, "roll_d3", return_value=2)

    dpytest.configure(bot)

    await dpytest.message("!roll d3")
    dpytest.verify_message("d3 (2) = `2`")

    await dpytest.message("!roll 1d3")
    dpytest.verify_message("d3 (2) = `2`")

    await dpytest.message("!roll 1d3+6")
    dpytest.verify_message("d3 (2)+6 = `8`")


@pytest.mark.asyncio
async def test_roll_d6(bot, mocker):
    mocker.patch.object(dice, "roll_d6", return_value=4)

    dpytest.configure(bot)

    await dpytest.message("!roll d6")
    dpytest.verify_message("d6 (4) = `4`")

    await dpytest.message("!roll 1d6")
    dpytest.verify_message("d6 (4) = `4`")

    await dpytest.message("!d6")
    dpytest.verify_message("d6 (4) = `4`")

    await dpytest.message("!roll d6+2")
    dpytest.verify_message("d6 (4)+2 = `6`")

    await dpytest.message("!roll 1d6-3")
    dpytest.verify_message("d6 (4)-3 = `1`")


@pytest.mark.asyncio
async def test_roll_2d6(bot, mocker):
    mocker.patch.object(dice, "roll_2d6", return_value=(1, 4, 5))

    dpytest.configure(bot)

    await dpytest.message("!roll 2d6")
    dpytest.verify_message("2d6 (1+4) = `5`")

    await dpytest.message("!2d6")
    dpytest.verify_message("2d6 (1+4) = `5`")

    await dpytest.message("!roll 2d6+3")
    dpytest.verify_message("2d6 (1+4)+3 = `8`")

    await dpytest.message("!roll 2d6-2")
    dpytest.verify_message("2d6 (1+4)-2 = `3`")


@pytest.mark.asyncio
async def test_roll_d66(bot, mocker):
    mocker.patch.object(dice, "roll_d66", return_value=23)

    dpytest.configure(bot)

    await dpytest.message("!roll d66")
    dpytest.verify_message("d66 = `23`")


@pytest.mark.asyncio
async def test_roll_d20(bot, mocker):
    mocker.patch.object(dice, "roll_d20", return_value=2)

    dpytest.configure(bot)

    await dpytest.message("!roll d20")
    dpytest.verify_message("d20 (2) = `2`")

    await dpytest.message("!roll 1d20")
    dpytest.verify_message("d20 (2) = `2`")

    await dpytest.message("!roll 1d20+6")
    dpytest.verify_message("d20 (2)+6 = `8`")


# @pytest.mark.asyncio
# async def test_roll_character(mocker):
#     tbot = TroikaBot("!")
#     mocker.patch.object(dice, "roll_d3", return_value=2)
#     mocker.patch.object(dice, "roll_d6", return_value=4)
#     mocker.patch.object(dice, "roll_2d6", return_value=(1, 4, 5))
#     mocker.patch.object(dice, "roll_d66", return_value=21)
#     tbot.add_cog(DiceCog(tbot))

#     dpytest.configure(tbot)

#     await dpytest.message("!roll character")
#     dpytest.verify_message(
#         """SKILL d3 (2)+3 = `5`
# STAMINA 2d6 (1+4)+12 = `17`
# LUCK d6 (4)+6 = `10`
# BACKGROUND d66 = `21`"""
#     )
