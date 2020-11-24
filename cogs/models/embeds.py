import random
import discord
from cogs.models.weapon import MIGHTY_BLOW_ROLL, FUMBLE_ROLL

from cogs.models.character import Item, ItemChoice, Skill, SpellSkill
from cogs.models.spell import Spell
from cogs.utils import oops
from cogs.utils.dice import RollResult


def render_item(item: Item) -> str:
    if isinstance(item, ItemChoice):
        choices = "\n".join([f"> {c.name}" for c in item.choices])
        return f"_One of:_\n{choices}"
    else:
        return item.name


def render_skill(skill: Skill) -> str:
    return f"**{skill.rank}** {skill.name}"


def render_spell_skill(skill: SpellSkill) -> str:
    return f"**{skill.rank}** {skill.name} ({skill.spell.cost})"


class EmbedWithAuthor(discord.Embed):
    """This was shamelessly borrowed from Avrae.
    An embed with author image and nickname set."""
    def __init__(self, ctx, **kwargs):
        super(EmbedWithAuthor, self).__init__(**kwargs)
        self.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar_url)
        self.colour = random.randint(0, 0xffffff)


class EmbedDamage(EmbedWithAuthor):
    """An embed to show the damage table for a given weapon."""
    def __init__(self, ctx, weapon, armor, bonus, **kwargs):
        super(EmbedDamage, self).__init__(ctx, **kwargs)
        roll = weapon.roll_damage(armor, bonus)
        damage_dealt = weapon.lookup_damage(roll.total)

        self.title = f"{weapon.name} Damage ({damage_dealt})"

        table = ""
        for indx, d in enumerate(weapon.damage):
            table += str(d) if indx + 1 is not roll.total else f"__**{d}**__"
            if len(weapon.damage) - 1 is not indx:
                table += " | "
        table = f" {table} "

        dmg_txt = f"Damage Dealt:\n{table}\n\n**{damage_dealt}** damage was dealt."

        roll_breakdown_txt = f"Roll Breakdown:\n{roll.result}"
        self.description = f"\n{roll_breakdown_txt}\n\n{dmg_txt}"


class EmbedSpell(EmbedWithAuthor):
    def __init__(self, ctx, spell: Spell = None, cast: RollResult = None, **kwargs):
        super(EmbedSpell, self).__init__(ctx, **kwargs)

        if spell:
            self.title = f"{spell.name} ({spell.cost})"
            self.description = spell.description

        if cast:
            oops_triggered = False
            self.title = self.title or "Spell Casting"
            if cast.total == 2:
                outcome = "**GUARANTEED SUCCESS** 2d6(1+1)"
            elif cast.total == 12:
                outcome = "**CATASTROPHIC FAILURE** 2d6(6+6)"
                oops_triggered = True
            else:
                outcome = cast.result

            self.add_field(name="Outcome", value=outcome, inline=False)

            if oops_triggered:
                roll, oops_str = oops.roll_oops()
                self.add_field(name="Ooops!", value=f"**{roll}:** {oops_str}", inline=False)


class EmbedOops(EmbedWithAuthor):
    def __init__(self, ctx, roll, oops, **kwargs):
        super(EmbedOops, self).__init__(ctx, **kwargs)

        self.title = "Oops!"
        self.description = f"**{roll}**: {self.oops}"


class EmbedAttack(EmbedWithAuthor):
    """An embed to show the attack result."""
    def __init__(self, ctx, attack_roll, attacker_mod, defense_roll, defender_mod, **kwargs):
        super(EmbedAttack, self).__init__(ctx, **kwargs)

        attack_total = attack_roll.total + attacker_mod
        defense_total = defense_roll.total + defender_mod

        description = f"**Attacker ({attack_total})**\n {attack_roll.result} + {attacker_mod} = {attack_total}\n\n"
        description += f"**Defender ({defense_total})**\n {defense_roll.result} + {defender_mod} = {defense_total}\n\n"

        winner = "ATTACKER" if attack_total > defense_total else "DEFENDER" if defense_total > attack_total else "TIE"
        mighty_blow = attack_roll.total == MIGHTY_BLOW_ROLL or defense_roll.total == MIGHTY_BLOW_ROLL
        fumble = attack_roll.total == FUMBLE_ROLL or defense_roll.total == FUMBLE_ROLL

        if winner == "TIE":
            if mighty_blow:
                self.title = "SPECTACULAR CLINCH!"
                description += " > Both Weapons shatter! (beasts lose 1d6 stamina)"
            elif fumble:
                self.title = "DOUBLE FUMBLE!"
                description += " > Both parties deal Damage to the other, adding +1 to their Damage Roll"
            else:
                self.title = "TIE"
                description += " > Nobody takes damage"
        elif mighty_blow:
            self.title = f"{winner} MIGHTY BLOW!"
            description += f" > {winner} wins the exchange and inflicts Double Damage"
        elif fumble:
            loser = "ATTACKER" if winner == "DEFENDER" else "DEFENDER"
            self.title = f"{loser} FUMBLE"
            description += f" > {loser} loses the exchange and {winner} adds +1 to their Damage Roll"
        else:
            self.title = f"{winner} WINS"
            description += " > Roll for damage"

        self.description = description


class EmbedInitShow(EmbedWithAuthor):
    """An embed to show a representation of the initiative bag."""
    def __init__(self, ctx, **kwargs):
        super(EmbedInitShow, self).__init__(ctx, **kwargs)


class EmbedCharacter(EmbedWithAuthor):
    """An embed to show a representative of a character"""
    def __init__(self, ctx, character, **kwargs):
        super(EmbedCharacter, self).__init__(ctx, **kwargs)

        self.title = f"**{character.background_roll}** {character.background_name}"

        self.description = f"""SKILL d3 ({character.skill-3})+3 = `{character.skill}`
STAMINA 2d6 ({character.stamina-12})+12 = `{character.stamina}`
LUCK d6 ({character.luck-6})+6 = `{character.luck}`
BACKGROUND d66 = `{character.background_roll}`

_{character.description}_
"""

        if len(character.specials) > 0:
            special = "\n".join([f"> {s}" for s in character.specials])
            self.add_field(name="Special", value=special, inline=False)

        if len(character.items) > 0:
            items = "\n".join([f"{render_item(i)}" for i in character.items])
            self.add_field(name="Items", value=items, inline=False)

        if len(character.skills) > 0:
            skills = "\n".join([render_skill(s) for s in character.skills])
            self.add_field(name="Skills", value=skills, inline=False)

        if len(character.spells) > 0:
            spells = "\n".join([render_spell_skill(s) for s in character.spells])
            self.add_field(name="Spells", value=spells, inline=False)
