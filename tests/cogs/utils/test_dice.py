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
    ('d6 monkeys', '2 monkeys'),
    ('There are 3d6 monkeys', 'There are 6 monkeys'),
    ('2d6 monkeys', '4 monkeys'),
    ('`2d6` monkeys', '`2d6` monkeys'),
    ('10d6 silver pence', '20 silver pence'),
    ('d3 Fighting', '2 Fighting')
])
def test_interpolate_dice(mocker, input, output):
    mocker.patch.object(dice, 'roll_die', return_value=2)
    assert dice.interpolate_dice(input) == output
