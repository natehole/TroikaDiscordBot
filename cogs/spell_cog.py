import re
from discord.ext import commands
from discord.ext.commands import ArgumentParsingError
from cogs.utils import oops, dice

SUCCESS_TOTAL = 2
OOPS_TOTAL = 12


class SpellCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # Lame but needed for mocks
    def roll_oops(self):
        return oops.roll_oops()

    @commands.command()
    async def spell(self, ctx, *, name: str):
        spell = self.bot.library.lookup_spell(name)
        if spell:
            await ctx.send(f"**{spell.name}** ({spell.cost})\n_{spell.description}_")
        else:
            await ctx.send(f"_Spell **{name}** not found. Check your spelling?_")

    @commands.command()
    async def cast(self, ctx, *, spell_str: str):
        r = re.match(r'([0-9]+)[ ]?(.+)?', spell_str)
        if not r:
            raise ArgumentParsingError("Usage: skill_points [spell_name]")

        skill_points = int(r.group(1))

        if r.group(2):
            await self.spell(ctx, name=r.group(2))

        # Look up spell in the library
        roll = dice.roll_under(skill_points)
        if roll.total == SUCCESS_TOTAL:
            await ctx.send("**GUARANTEED SUCCESS** 2d6(1+1)")
        elif roll.total == OOPS_TOTAL:
            await ctx.send("**CATASTROPHIC FAILURE** 2d6(6+6)")
            await self.oops(ctx)
        else:
            await ctx.send(roll.result)

    @commands.command()
    async def oops(self, ctx):
        roll, oops = self.roll_oops()
        await ctx.send(f"OOPS (**{roll}**): `{oops}`")


def setup(bot):
    bot.add_cog(SpellCog(bot))
