import random
import discord
from cogs.models.weapon import MIGHTY_BLOW_ROLL, FUMBLE_ROLL


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
        for indx, d in enumerate(weapon.damage_table):
            table += str(d) if indx + 1 is not roll.total else f"__**{d}**__"
            if len(weapon.damage_table) - 1 is not indx:
                table += " | "
        table = f" {table} "

        dmg_txt = f"Damage Dealt:\n{table}\n\n**{damage_dealt}** damage was dealt."

        roll_breakdown_txt = f"Roll Breakdown:\n{roll.result}"
        self.description = f"\n{roll_breakdown_txt}\n\n{dmg_txt}"


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
