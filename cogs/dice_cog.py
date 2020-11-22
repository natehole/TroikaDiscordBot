import re
from discord.ext import commands
from discord.ext.commands import ArgumentParsingError

from cogs.utils import dice
from cogs.models.character import Character

def modifier_string(modifier):
    if modifier == 0:
        return ""
    elif modifier > 0:
        return f"+{modifier}"
    else:
        return f"{modifier}"


class DiceCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(
        name="roll",
        aliases=["r", "dice"],
        brief="Roll dice manually",
        usage="roll d6|d6+4|2d6|d66|d3",
    )
    async def roll(self, ctx, *, query: str):
        """Rolls the dice"""
        CHARACTER_REGEXP = re.compile("char(acter)?( [^0-9][^ ]*)?( [0-9]+)?")
        D2_REGEXP = re.compile("1?d2([+-][0-9]+)?$")
        D3_REGEXP = re.compile("1?d3([+-][0-9]+)?$")
        D6_REGEXP = re.compile("1?d6([+-][0-9]+)?$")
        TWO_D6_REGEXP = re.compile("2d6([+-][0-9]+)?$")
        D20_REGEXP = re.compile("1?d20([+-][0-9]+)?$")
        D66_REGEXP = re.compile("d66$")

        # initialize
        regexp_matched = False
        modifier = 0

        match = CHARACTER_REGEXP.match(query)
        if match:
            if match.group(2):
                key = match.group(2).lstrip()
            else:
                key = 'base'

            if match.group(3):
                bg_roll = int(match.group(3).lstrip())
            else:
                bg_roll = dice.roll_d66()

            regexp_matched = True
            library = self.bot.get_cog('LibraryCog')
            compendium = library.find_compendium(key)

            if compendium:
                background = compendium.lookup_background(bg_roll)
                if background:
                    character = Character.generate(compendium, background)
                    await ctx.send(character)
                else:
                    await ctx.send("BACKGROUND d66 = `{bg_roll}`\n_No background found..._")
            else:
                await ctx.send(f"No compendium found for `{key}`")

        match = D66_REGEXP.match(query)
        if match:
            regexp_matched = True
            total = dice.roll_d66()
            await ctx.send(f"d66 = `{total}`")

        match = D2_REGEXP.match(query)
        if not regexp_matched and match:
            regexp_matched = True
            roll = dice.roll_d2()

            if match.group(1):
                modifier = int(match.group(1))

            await ctx.send(
                f"d2 ({roll}){modifier_string(modifier)} = `{roll+modifier}`"
            )

        match = D3_REGEXP.match(query)
        if not regexp_matched and match:
            regexp_matched = True
            roll = dice.roll_d3()

            if match.group(1):
                modifier = int(match.group(1))

            await ctx.send(
                f"d3 ({roll}){modifier_string(modifier)} = `{roll+modifier}`"
            )

        match = D6_REGEXP.match(query)
        if not regexp_matched and match:
            regexp_matched = True
            roll = dice.roll_d6()

            if match.group(1):
                modifier = int(match.group(1))

            await ctx.send(
                f"d6 ({roll}){modifier_string(modifier)} = `{roll+modifier}`"
            )

        match = TWO_D6_REGEXP.match(query)
        if not regexp_matched and match:
            regexp_matched = True
            r1, r2, total = dice.roll_2d6()

            if match.group(1):
                modifier = int(match.group(1))

            await ctx.send(
                f"2d6 ({r1}+{r2}){modifier_string(modifier)} = `{total+modifier}`"
            )

        match = D20_REGEXP.match(query)
        if not regexp_matched and match:
            regexp_matched = True
            roll = dice.roll_d20()

            if match.group(1):
                modifier = int(match.group(1))

            await ctx.send(
                f"d20 ({roll}){modifier_string(modifier)} = `{roll+modifier}`"
            )

        if not regexp_matched:
            raise ArgumentParsingError(f"Unable to understand your command: `{query}`")

    @commands.command(name="d6", aliases=["1d6"], hidden=True)
    async def roll_d6(self, ctx):
        await ctx.invoke(self.bot.get_command("roll"), query="d6")

    @commands.command(name="2d6", hidden=True)
    async def roll_2d6(self, ctx):
        await ctx.invoke(self.bot.get_command("roll"), query="2d6")

    @commands.command(name="character", aliases=['char'], hidden=True)
    async def roll_character(self, ctx):
        await ctx.invoke(self.bot.get_command("roll"), query="character")


def setup(bot):
    bot.add_cog(DiceCog(bot))
