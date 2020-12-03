"""A place for useful utility functions"""
import random
import re
from functools import reduce
import operator


class RollResult:
    """A somewhat compatible class equivalent to d20"""

    def __init__(self, total, result):
        self.total = total
        self.result = result


def roll_die(sides: int) -> int:
    return random.randint(1, sides)


def roll_d2():
    """Rolls a d2"""
    return roll_die(2)


def roll_d3():
    """Rolls a single d3"""
    return roll_die(3)


def roll_d6():
    """Rolls a single d6"""
    return roll_die(6)


def roll_2d6():
    """Rolls 2d6. Returns first die, second die, total of both die"""
    die1 = roll_d6()
    die2 = roll_d6()

    return die1, die2, die1 + die2


def roll_under(target):
    d1, d2, total = roll_2d6()
    if total <= target:
        return RollResult(total, f"**SUCCESS** 2d6({d1}+{d2}) = `{total}` ≤ `{target}`")
    else:
        return RollResult(total, f"**FAILURE** 2d6({d1}+{d2}) = `{total}` > `{target}`")


def roll_d20():
    """Rolls a d20"""
    return roll_die(20)


def roll_d66():
    """Rolls a d66. Returns a single value"""
    die1 = roll_d6()
    die2 = roll_d6()
    total = (die1 * 10) + die2
    return total


def _replace_fragment(text):
    r = re.match(r'([0-9]*)d([0-9]+)$', text)
    if r:
        if r.group(1):
            rolls = int(r.group(1))
        else:
            rolls = 1

        sides = int(r.group(2))
        total = reduce(operator.add, [roll_die(sides) for r in range(rolls)])
        return f"{total}"
    else:
        return text


def interpolate_dice(text):
    """Replace dice strings with rolls"""
    pieces = re.split(r'([`]?[0-9]*d[0-9]+[`]?)', text)
    out_pieces = [_replace_fragment(t) for t in pieces]
    return ''.join(out_pieces)
