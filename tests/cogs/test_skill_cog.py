import discord.ext.test as dpytest
import pytest

from cogs.utils import dice


@pytest.mark.asyncio
async def test_skill(bot, mocker):
    mocker.patch.object(dice, "roll_2d6", return_value=(1, 3, 4))

    dpytest.configure(bot)

    await dpytest.message("!skill 4")
    dpytest.verify_message("**SUCCESS** 2d6(1+3) = `4` ≤ `4`")

    await dpytest.message("!skill 3")
    dpytest.verify_message("**FAILURE** 2d6(1+3) = `4` > `3`")


@pytest.mark.asyncio
async def test_better(bot, mocker):
    mocker.patch.object(dice, "roll_2d6", return_value=(4, 3, 7))

    dpytest.configure(bot)

    await dpytest.message("!better 6")
    dpytest.verify_message("**SUCCESS** 2d6(4+3) = `7` > `6`. Increase advanced skill by 1")

    await dpytest.message("!better 7")
    dpytest.verify_message("**FAILURE** 2d6(4+3) = `7` ≤ `7`. Advanced skill unchanged")


@pytest.mark.asyncio
async def test_better_more(bot, mocker):
    mocker.patch.object(dice, "roll_2d6", return_value=(6, 6, 12))

    dpytest.configure(bot)

    await dpytest.message("!better 13")
    dpytest.verify_message("**SUCCESS** 2d6(6+6)+2d6(6+6) = `24`. Increase advanced skill by 1")

    mocker.patch.object(dice, "roll_2d6", side_effect=((6, 6, 12), (6, 5, 11)))
    await dpytest.message("!better 12")
    dpytest.verify_message("**FAILURE** 2d6(6+6)+2d6(6+5) = `23`. Advanced skill unchanged")
