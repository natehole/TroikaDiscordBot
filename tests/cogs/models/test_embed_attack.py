import pytest

from cogs.utils import dice
from cogs.models.embeds import EmbedAttack


#@pytest.mark.parametrize("attacker_roll,defender_roll,attacker_skill,defender_skill,desc,title", [
    #(["**6+6**", 12], ["**6+6**", 12], 3, 3, "**Attacker (15)**\n 12 + 3 = 15\n**Defender (15)**\n 12 + 3 = 15\n > Both weapons shatter! (beasts lose 1d6 stamina)", "SPECTACULAR CLINCH"),
    # ([6, 6, 12], [6, 5, 11], 1, 3, "Attacker: 2d6(**6+6**) = 12 + 1 = `13`\nDefender: 2d6(6+5) = 11 + 3 = `14`\n**ATTACKER MIGHTY BLOW** Attacker wins and should score double damage", "FPP"),
    # ([5, 6, 11], [6, 6, 12], 3, 1, "Attacker: 2d6(5+6) = 11 + 3 = `14`\nDefender: 2d6(**6+6**) = 12 + 1 = `13`\n**DEFENDER MIGHTY BLOW** Defender wins and should score double damage", "FOO"),
    # ([1, 1, 2], [1, 1, 2], 1, 2, "Attacker: 2d6(**1+1**) = 2 + 1 = `3`\nDefender: 2d6(**1+1**) = 2 + 2 = `4`\n**DOUBLE FUMBLE** Both sides roll damage with a +1 bonus", "DOUBLE FUMBLE"),
    # ([1, 1, 2], [1, 2, 3], 5, 1, "Attacker: 2d6(**1+1**) = 2 + 5 = `7`\nDefender: 2d6(1+2) = 3 + 1 = `4`\n**ATTACKER FUMBLE** Attacker loses and defender adds a +1 bonus to their damage roll", "FOO"),
    # ([1, 2, 3], [1, 1, 2], 1, 5, "Attacker: 2d6(1+2) = 3 + 1 = `4`\nDefender: 2d6(**1+1**) = 2 + 5 = `7`\n**DEFENDER FUMBLE** Defender loses and attacker adds a +1 bonus to their damage roll", "FOO"),
    # ([2, 3, 5], [2, 3, 5], 3, 2, "Attacker: 2d6(2+3) = 5 + 3 = `8`\nDefender: 2d6(2+3) = 5 + 2 = `7`\n**ATTACKER WINS** Roll for damage", "FOO"),
    # ([2, 3, 5], [2, 3, 5], 2, 3, "Attacker: 2d6(2+3) = 5 + 2 = `7`\nDefender: 2d6(2+3) = 5 + 3 = `8`\n**DEFENDER WINS** Roll for damage", "FOO"),
#     # ([2, 3, 5], [4, 3, 7], 3, 1, "Attacker: 2d6(2+3) = 5 + 3 = `8`\nDefender: 2d6(4+3) = 7 + 1 = `8`\n> Nobody takes damage", "TIE")
# ])
# def test_attack(bot, ctx, mocker, attacker_roll, defender_roll, attacker_skill, defender_skill, desc, title):
#     mocker.patch.object(dice, 'roll_2d6', side_effect=[attacker_roll, defender_roll])

#     a_roll = dice.RollResult(attacker_roll[1], attacker_roll[0])
#     d_roll = dice.RollResult(defender_roll[1], defender_roll[0])

#     embed = EmbedAttack(ctx, a_roll, attacker_skill, d_roll, defender_skill)
#     assert embed.description == desc
#     assert embed.title == title
