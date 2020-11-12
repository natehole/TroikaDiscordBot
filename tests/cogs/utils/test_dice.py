import pytest
from cogs.utils import dice


def test_roll_d2():
    for _ in range(100):
        r = dice.roll_d2()
        assert r >= 1 and r <= 2


def test_roll_d3():
    for _ in range(100):
        r = dice.roll_d3()
        assert r >= 1 and r <= 3


def test_roll_d6():
    for _ in range(100):
        r = dice.roll_d6()
        assert r >= 1 and r <= 6


def test_roll_2d6():
    for _ in range(100):
        r1, r2, r3 = dice.roll_2d6()
        assert r1 >= 1 and r1 <= 6
        assert r2 >= 1 and r2 <= 6
        assert r3 == r1 + r2


def test_roll_d66():
    for _ in range(100):
        r = dice.roll_d66()
        assert r >= 11 and r <= 66


def test_roll_d20():
    for _ in range(100):
        r = dice.roll_d20()
        assert r >= 1 and r <= 20


@pytest.mark.parametrize('input,output', [
    ('d6 monkeys', '`3` monkeys'),
    ('There are 3d6 monkeys', 'There are `9` monkeys'),
    ('2d6 monkeys', '`6` monkeys'),
    ('`2d6` monkeys', '`2d6` monkeys'),
    ('10d6 silver pence', '`30` silver pence')
])
def test_insert_rolls(mocker, input, output):
    mocker.patch.object(dice, 'roll_d6', return_value=3)
    assert dice.replace_rolls(input) == output
