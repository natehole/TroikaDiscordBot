from typing import Optional

import re
from discord.ext import commands
from discord.ext.commands import ArgumentParsingError
from cogs.utils import oops, dice
from cogs.models.embeds import EmbedSpell, EmbedOops
from cogs.models.spell import Spell

SUCCESS_TOTAL = 2
OOPS_TOTAL = 12


class SpellCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def spell(self, ctx, *, name: str):
        library = self.bot.get_cog('LibraryCog')
        spell = library.lookup_spell(name)
        if spell:
            embed = EmbedSpell(ctx, spell=spell)
            await ctx.send(embed=embed)
        else:
            await ctx.send(f"_Spell **{name}** not found. Check your spelling?_")

    @commands.command()
    async def cast(self, ctx, *, spell_str: str):
        r = re.match(r'([0-9]+)[ ]?(.+)?', spell_str)
        if not r:
            raise ArgumentParsingError("Usage: skill_points [spell_name]")

        skill_points: int = int(r.group(1))
        spell: Optional[Spell] = None

        if r.group(2):
            library = self.bot.get_cog('LibraryCog')
            spell = library.lookup_spell(r.group(2))

        # Look up spell in the library
        roll = dice.roll_under(skill_points)
        embed = EmbedSpell(ctx, spell=spell, cast=roll)
        await ctx.send(embed=embed)

    @commands.command()
    async def oops(self, ctx):
        roll, oops_str = oops.roll_oops()
        embed = EmbedOops(ctx, roll, oops_str)
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(SpellCog(bot))
