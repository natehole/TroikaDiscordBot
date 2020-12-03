import pytest

from cogs.utils import dice
from cogs.models.embeds import EmbedAttack


@pytest.mark.parametrize("attacker_roll,defender_roll,attacker_skill,defender_skill,desc,title", [
    ([6, 6, 12], [6, 6, 12], 3, 3, "**Attacker (15)**\n 2d6(**6+6**) = 12 + 3 = 15\n\n**Defender (15)**\n 2d6(**6+6**) = 12 + 3 = 15\n\n > Both Weapons shatter! (beasts lose 1d6 stamina)", "SPECTACULAR CLINCH!"),
    ([6, 6, 12], [6, 5, 11], 1, 3, "**Attacker (13)**\n 2d6(**6+6**) = 12 + 1 = 13\n\n**Defender (14)**\n 2d6(6+5) = 11 + 3 = 14\n\n > ATTACKER wins the exchange and inflicts Double Damage", "ATTACKER MIGHTY BLOW!"),
    ([5, 6, 11], [6, 6, 12], 3, 1, "**Attacker (14)**\n 2d6(5+6) = 11 + 3 = 14\n\n**Defender (13)**\n 2d6(**6+6**) = 12 + 1 = 13\n\n > DEFENDER wins the exchange and inflicts Double Damage", "DEFENDER MIGHTY BLOW!"),
    ([1, 1, 2], [1, 1, 2], 1, 2, "**Attacker (3)**\n 2d6(**1+1**) = 2 + 1 = 3\n\n**Defender (4)**\n 2d6(**1+1**) = 2 + 2 = 4\n\n > Both parties deal Damage to the other, adding +1 to their Damage Roll", "DOUBLE FUMBLE!"),
    ([1, 1, 2], [1, 2, 3], 5, 1, "**Attacker (7)**\n 2d6(**1+1**) = 2 + 5 = 7\n\n**Defender (4)**\n 2d6(1+2) = 3 + 1 = 4\n\n > ATTACKER loses the exchange and DEFENDER adds +1 to their Damage Roll", "ATTACKER FUMBLE"),
    ([1, 2, 3], [1, 1, 2], 1, 5, "**Attacker (4)**\n 2d6(1+2) = 3 + 1 = 4\n\n**Defender (7)**\n 2d6(**1+1**) = 2 + 5 = 7\n\n > DEFENDER loses the exchange and ATTACKER adds +1 to their Damage Roll", "DEFENDER FUMBLE"),
    ([2, 3, 5], [2, 3, 5], 3, 2, "**Attacker (8)**\n 2d6(2+3) = 5 + 3 = 8\n\n**Defender (7)**\n 2d6(2+3) = 5 + 2 = 7\n\n > Roll for damage", "ATTACKER WINS"),
    ([2, 3, 5], [2, 3, 5], 2, 3, "**Attacker (7)**\n 2d6(2+3) = 5 + 2 = 7\n\n**Defender (8)**\n 2d6(2+3) = 5 + 3 = 8\n\n > Roll for damage", "DEFENDER WINS"),
    ([2, 3, 5], [4, 3, 7], 3, 1, "**Attacker (8)**\n 2d6(2+3) = 5 + 3 = 8\n\n**Defender (8)**\n 2d6(4+3) = 7 + 1 = 8\n\n > Nobody takes damage", "TIE")
])
def test_attack(bot, ctx, mocker, attacker_roll, defender_roll, attacker_skill, defender_skill, desc, title):
    mocker.patch.object(dice, 'roll_2d6', side_effect=[attacker_roll, defender_roll])

    embed = EmbedAttack(ctx, attacker_skill, defender_skill)
    assert embed.title == title
    assert embed.description == desc
