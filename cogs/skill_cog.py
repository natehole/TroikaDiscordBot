from discord.ext import commands

from cogs.utils import dice


class SkillCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="skill",
                      aliases=["s", "sk"],
                      brief="Test to roll under a specific skill",
                      usage="skill skill_level")
    async def skill(self, ctx, skill: int):
        await ctx.send(dice.roll_under(skill).result)


    @commands.command(name="better",
                      aliases=["improve", "advance", "adv"],
                      brief="Test to see if you can improve a special skill by rolling over",
                      usage="better skill_level")
    async def better(self, ctx, skill: int):
        d1, d2, total = dice.roll_2d6()

        if skill < 12:
            if total > skill:
                await ctx.send(f"**SUCCESS** 2d6({d1}+{d2}) = `{total}` > `{skill}`. Increase advanced skill by 1")
            else:
                await ctx.send(f"**FAILURE** 2d6({d1}+{d2}) = `{total}` ≤ `{skill}`. Advanced skill unchanged")
        else:
            d3, d4, total2 = dice.roll_2d6()
            if total + total2 == 24:
                await ctx.send(f"**SUCCESS** 2d6({d1}+{d2})+2d6({d3}+{d4}) = `{total+total2}`. Increase advanced skill by 1")
            else:
                await ctx.send(f"**FAILURE** 2d6({d1}+{d2})+2d6({d3}+{d4}) = `{total+total2}`. Advanced skill unchanged")

def setup(bot):
    bot.add_cog(SkillCog(bot))
