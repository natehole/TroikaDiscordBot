import discord.ext.test as dpytest
import pytest

from bot import TroikaBot
from cogs.utils import dice
from cogs.skill_cog import SkillCog


@pytest.mark.asyncio
async def test_skill(mocker):
    tbot = TroikaBot('!')
    mocker.patch.object(dice, "roll_2d6", return_value=(1, 3, 4))
    tbot.add_cog(SkillCog(tbot))

    dpytest.configure(tbot)

    await dpytest.message("!skill 4")
    dpytest.verify_message("**SUCCESS** 2d6(1+3) = `4` ≤ `4`")

    await dpytest.message("!skill 3")
    dpytest.verify_message("**FAILURE** 2d6(1+3) = `4` > `3`")


@pytest.mark.asyncio
async def test_better(mocker):
    tbot = TroikaBot('!')
    mocker.patch.object(dice, "roll_2d6", return_value=(4, 3, 7))
    tbot.add_cog(SkillCog(tbot))

    dpytest.configure(tbot)

    await dpytest.message("!better 6")
    dpytest.verify_message("**SUCCESS** 2d6(4+3) = `7` > `6`. Increase advanced skill by 1")

    await dpytest.message("!better 7")
    dpytest.verify_message("**FAILURE** 2d6(4+3) = `7` ≤ `7`. Advanced skill unchanged")


@pytest.mark.asyncio
async def test_better_more(mocker):
    tbot = TroikaBot('!')
    mocker.patch.object(dice, "roll_2d6", return_value=(6, 6, 12))
    tbot.add_cog(SkillCog(tbot))

    dpytest.configure(tbot)

    await dpytest.message("!better 13")
    dpytest.verify_message("**SUCCESS** 2d6(6+6)+2d6(6+6) = `24`. Increase advanced skill by 1")

    mocker.patch.object(dice, "roll_2d6", side_effect=((6, 6, 12), (6, 5, 11)))
    await dpytest.message("!better 12")
    dpytest.verify_message("**FAILURE** 2d6(6+6)+2d6(6+5) = `23`. Advanced skill unchanged")
