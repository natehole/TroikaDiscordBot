from typing import Optional

from discord.ext import commands

from cogs.models.spell import Spell
from cogs.models.weapon import Weapon
from cogs.models.library import Library

class LibraryCog(commands.Cog):
    def __init__(self, bot):
        self.library = Library()
        self.library.load_compendium('base')

    @commands.command
    async def load(self, ctx, *, path):
        try:
            await ctx.send(f"Loading compendium at {path}")
            self.library.load_compendium(path)
        except ValueError as err:
            await ctx.send(f"Exception: {err}")

    def add_temp_weapon(self, weapon: Weapon):
        self.library.add_temp_weapon(weapon)

    def lookup_weapon(self, weapon_name: str) -> Optional[Weapon]:
        return self.library.lookup_weapon(weapon_name)

    def lookup_spell(self, spell_name: str) -> Optional[Spell]:
        return self.library.lookup_spell(spell_name)


def setup(bot):
    bot.add_cog(LibraryCog(bot))
