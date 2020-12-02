from dataclasses import dataclass
import pytest

from discord.user import BaseUser
from discord.ext.commands import Context

from bot import TroikaBot
from cogs.battle_cog import BattleCog
from cogs.library_cog import LibraryCog
from cogs.luck_cog import LuckCog
from cogs.dice_cog import DiceCog
from cogs.define_cog import DefineCog
from cogs.initiative_cog import InitiativeCog
from cogs.skill_cog import SkillCog
from cogs.spell_cog import SpellCog


@pytest.fixture(scope="function")
def bot():
    bot = TroikaBot('!')
    bot.add_cog(BattleCog(bot))
    bot.add_cog(LibraryCog(bot))
    bot.add_cog(LuckCog(bot))
    bot.add_cog(DiceCog(bot))
    bot.add_cog(DefineCog(bot))
    bot.add_cog(InitiativeCog(bot))
    bot.add_cog(SkillCog(bot))
    bot.add_cog(SpellCog(bot))
    return bot



@dataclass
class MockUser:
    display_name = 'testuser'
    avatar_url = 'http://example.com/testuser'


@dataclass
class MockMessage:
    _state = None


class MockContext:
    def __init__(self, bot=None, user=None):
        self.bot = bot
        self.user = user

    @property
    def author(self):
        return self.user


@pytest.fixture(scope="function")
def user():
    return MockUser()


@pytest.fixture(scope="function")
def ctx(bot, user):
    return MockContext(bot, user)
