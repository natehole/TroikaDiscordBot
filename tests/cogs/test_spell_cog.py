import discord.ext.test as dpytest
import bot
import pytest

from cogs.utils import dice
from cogs.spell_cog import SpellCog
from cogs.library_cog import LibraryCog


@pytest.mark.asyncio
async def test_spell_cog(mocker):
    tbot = bot.TroikaBot('!')
    oops_cog = SpellCog(tbot)
    tbot.add_cog(oops_cog)
    tbot.add_cog(LibraryCog(tbot))

    mocker.patch.object(oops_cog, 'roll_oops', return_value=(23, "A very surprised orc appears."))
    dpytest.configure(tbot)

    await dpytest.message("!oops")
    dpytest.verify_message("OOPS (**23**): `A very surprised orc appears.`")

    await dpytest.message("!spell darkness")
    dpytest.verify_message("**Darkness** (3)\n_Summon a stationary, perfect sphere of darkness up to five metres from the wizard for up to 3 minutes._")

    mocker.patch.object(dice, 'roll_2d6', return_value=(1, 2, 3))
    await dpytest.message("!cast 7")
    dpytest.verify_message("**SUCCESS** 2d6(1+2) = `3` ≤ `7`")

    mocker.patch.object(dice, 'roll_2d6', return_value=(5, 5, 10))
    await dpytest.message("!cast 7 read entrails")
    dpytest.verify_message("**Read Entrails** (1)\n_The wizard can get the answer to one question from the entrails of a living creature. The size and importance of the creature influences the level of knowledge gained. Small, common animals are able to offer yes or no answers, oxen can predict things obtusely, lamassu may offer explicit and thorough advice._")
    dpytest.verify_message("**FAILURE** 2d6(5+5) = `10` > `7`")

    mocker.patch.object(dice, "roll_2d6", return_value=(1, 1, 2))
    await dpytest.message("!cast 1")
    dpytest.verify_message("**GUARANTEED SUCCESS** 2d6(1+1)")

    mocker.patch.object(dice, "roll_2d6", return_value=(6, 6, 12))
    await dpytest.message("!cast 7")
    dpytest.verify_message("**CATASTROPHIC FAILURE** 2d6(6+6)")
    dpytest.verify_message("OOPS (**23**): `A very surprised orc appears.`")
