import re

from discord.ext import commands
from discord.ext.commands import NoPrivateMessage, ArgumentParsingError, BadArgument

from cogs.utils import dice
from cogs.models.weapon import ARMOR_REGEXP_STRING
from cogs.models.embeds import EmbedDamage, EmbedAttack

class BattleCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # Borrowed this from avrae
    async def cog_check(self, ctx):
        if ctx.guild is None:
            raise NoPrivateMessage()
        return True

    @commands.command(name="damage",
                      aliases=["d", "dam"],
                      brief="Rolls and computes the damage from a weapon against an armor type with an optional bonus. Arguments: weapon [light|medium|heavy] [bonus]",
                      usage="weapon name [light|medium|heavy] [+1]")
    async def damage(self, ctx, *, arg_str):
        # DEFINE REGEXPS
        DAMAGE_REGEXP_TWO_INTS = re.compile("(.+) ([+-]?[0-9]+) ([+-]?[0-9]+)")
        DAMAGE_REGEXP_BONUS_ONLY = re.compile("(.+) ([+-]?[0-9]+)")
        DAMAGE_REGEXP_ARMOR_BONUS = re.compile(f"(.+) {ARMOR_REGEXP_STRING} ([+-]?[0-9]+)", flags=re.IGNORECASE)
        DAMAGE_REGEXP_ARMOR = re.compile(f"(.+) ({ARMOR_REGEXP_STRING})", flags=re.IGNORECASE)
        DAMAGE_REGEXP_NONE = re.compile("(.+)")

        # initialize
        regexp_matched = False
        armor = ''

        bonus = 0

        # weapon, armor offset, bonus offset
        match = DAMAGE_REGEXP_TWO_INTS.match(arg_str)
        if match:
            regexp_matched = True
            weapon_name = match.group(1)
            armor = match.group(2)
            bonus = int(match.group(3))

        match = DAMAGE_REGEXP_ARMOR_BONUS.match(arg_str)
        if not regexp_matched and match:
            regexp_matched = True
            weapon_name = match.group(1)
            armor = match.group(2)
            bonus = int(match.group(3))

        match = DAMAGE_REGEXP_ARMOR.match(arg_str)
        if not regexp_matched and match:
            regexp_matched = True
            weapon_name = match.group(1)
            armor = match.group(2)
            bonus = 0

        match = DAMAGE_REGEXP_BONUS_ONLY.match(arg_str)
        if not regexp_matched and match:
            regexp_matched = True
            weapon_name = match.group(1)
            armor = "No"
            bonus = int(match.group(2))

        match = DAMAGE_REGEXP_NONE.match(arg_str)
        if not regexp_matched and match:
            regexp_matched = True
            weapon_name = match.group(1)
            armor = "No"
            bonus = 0

        if not regexp_matched:
            raise ArgumentParsingError("Unable to parse the inputs. Please check what you wrote.")

        library = self.bot.get_cog('LibraryCog')
        weapon = library.lookup_weapon(weapon_name)
        if weapon is None:
            raise BadArgument(f"Unable to find a weapon definition for `{weapon_name}`. Check your spelling?")

        embed = EmbedDamage(ctx, weapon, armor, bonus)
        await ctx.send(embed=embed)

    def roll_2d6(self):
        dice1, dice2, total = dice.roll_2d6()

        dice_string = ''
        if (dice1 == 6 and dice2 == 6) or (dice1 == 1 and dice2 == 1):
            dice_string = f"**{dice1}+{dice2}**"
        else:
            dice_string = f"{dice1}+{dice2}"

        return dice.RollResult(total, f"2d6({dice_string}) = {total}")

    @commands.command(name="attack",
                      aliases=["a", "att"],
                      brief="Rolls and computes the winner of an attack. Arguments: attack attacker_skill_mod defender_skill_mod",
                      usage="attack attacker_skill_mod defender_skill_mod")
    async def attack(self, ctx, attacker_mod: int, defender_mod: int):
        attack_roll = self.roll_2d6()
        defense_roll = self.roll_2d6()

        embed = EmbedAttack(ctx, attack_roll, attacker_mod, defense_roll, defender_mod)
        await ctx.send(embed=embed)


def setup(bot):
    '''Called by extension setup'''
    bot.add_cog(BattleCog(bot))
