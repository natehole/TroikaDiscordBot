import discord.ext.test as dpytest
import pytest

from bot import TroikaBot
from cogs.models.initiative_tracker import InitiativeTracker, END_OF_ROUND_TOKEN
from cogs.initiative_cog import InitiativeCog, NO_INIT_TRACKER_MESSAGE, NOT_IN_ROUND_MESSAGE
from cogs.library_cog import LibraryCog

@pytest.fixture(scope="function")
def bot():
   bot = TroikaBot('!')
   bot.add_cog(LibraryCog(bot))
   bot.add_cog(InitiativeCog(bot))
   return bot


@pytest.mark.asyncio
async def test_init_cog_normal(bot, mocker):
    dpytest.configure(bot)

    await dpytest.message("!i begin")
    dpytest.verify_message("Battle started. Now add tokens with !init add...")

    await dpytest.message("!i add 4 Goblin 6 Ogre 2 Fighter")
    dpytest.verify_message("Added 4 Goblin tokens.\nAdded 6 Ogre tokens.\nAdded 2 Fighter tokens.\n")

    await dpytest.message("!i add 2 Fred Wizard 2 Henchman")
    dpytest.verify_message("Added 2 Fred Wizard tokens.\nAdded 2 Henchman tokens.\n")

    def fixed_shuffle(self):
        self.round_bag = ["Goblin", "Fighter", END_OF_ROUND_TOKEN]

    mocker.patch.object(InitiativeTracker, "shuffle_tokens", new=fixed_shuffle)

    await dpytest.message("!i round")
    dpytest.verify_message("Starting round 1 of combat! Shuffling the bag...")
    dpytest.verify_message("Current Turn: **Goblin**")

    await dpytest.message("!i draw")
    dpytest.verify_message("Current Turn: **Fighter**")

    await dpytest.message("!i current")
    dpytest.verify_message('ROUND 1 current: **Fighter** recent: Goblin')

    await dpytest.message("!i draw")
    dpytest.verify_message("END OF ROUND 1")

    await dpytest.message("!i draw")
    dpytest.verify_message(NOT_IN_ROUND_MESSAGE)

    await dpytest.message("!i current")
    dpytest.verify_message(NOT_IN_ROUND_MESSAGE)

    await dpytest.message("!i end")
    dpytest.verify_message("Battle is now ended")


@pytest.mark.asyncio
async def test_init_call_when_ended(bot):
    dpytest.configure(bot)

    await dpytest.message("!i add 4 Ogre")
    dpytest.verify_message(NO_INIT_TRACKER_MESSAGE)

    await dpytest.message("!i round")
    dpytest.verify_message(NO_INIT_TRACKER_MESSAGE)

    await dpytest.message("!i draw")
    dpytest.verify_message(NO_INIT_TRACKER_MESSAGE)

    await dpytest.message("!i round")
    dpytest.verify_message(NO_INIT_TRACKER_MESSAGE)

    await dpytest.message("!i current")
    dpytest.verify_message(NO_INIT_TRACKER_MESSAGE)


@pytest.mark.asyncio
async def test_init_cog_remove_tokens(bot):
    '''Test removing the exact number of tokens of a certain type'''
    dpytest.configure(bot)

    await dpytest.message("!i begin")
    dpytest.verify_message("Battle started. Now add tokens with !init add...")

    await dpytest.message("!i add 4 Goblin 6 Ogre 2 Troll 2 Vince McFighty")
    dpytest.verify_message("Added 4 Goblin tokens.\nAdded 6 Ogre tokens.\nAdded 2 Troll tokens.\nAdded 2 Vince McFighty tokens.\n")

    await dpytest.message("!i remove 4 Ogre")
    dpytest.verify_message("Removed 4 Ogre tokens from the bag (2 left)")

    await dpytest.message("!i remove 4 Ogre")
    dpytest.verify_message("You asked to remove 4 Ogre tokens, but only 2 were in the bag (0 left)")

    await dpytest.message("!i remove 4 Goblin")
    dpytest.verify_message("Removed all 4 Goblin tokens from the bag (0 left)")

    await dpytest.message("!i remove 2 Vince McFighty")
    dpytest.verify_message("Removed all 2 Vince McFighty tokens from the bag (0 left)")
