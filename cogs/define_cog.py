import re

from discord.ext import commands
from discord.ext.commands import ArgumentParsingError

from cogs.models.weapon import Weapon


class DefineCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.group(aliases=['def'], invoke_without_command=True)
    async def define(self, ctx):
        await ctx.send(f"Incorrect usage. Use `{ctx.prefix}help define` for help.")

    @define.command(aliases=["w"])
    async def weapon(self, ctx, *, arg):
        weapon_regex = r'([^0-9]+) ([0-9]+) ([0-9]+) ([0-9]+) ([0-9]+) ([0-9]+) ([0-9]+) ([0-9]+)( ignore)?$'

        r = re.match(weapon_regex, arg)
        if not r:
            raise ArgumentParsingError("Argument should be `weapon name 1 2 3 4 5 6 7 [ignore]`")

        weapon_name = r.group(1)
        damage_table = [int(r.group(2)), int(r.group(3)), int(r.group(4)), int(r.group(5)),
                        int(r.group(6)), int(r.group(7)), int(r.group(8))]
        ignore_armor = r.group(9) is not None

        weapon = Weapon(damage_table, name=weapon_name, ignore_armor=ignore_armor)

        library = self.bot.get_cog('LibraryCog')
        library.add_temp_weapon(weapon)
        await ctx.send(f"Added weapon `{weapon_name}` damage `{damage_table}` ignore_armor={ignore_armor}")


def setup(bot):
    bot.add_cog(DefineCog(bot))
