from cogs.models.compendium import Compendium, normalize


def test_normalize():
    assert normalize("Fear") == "fear"
    assert normalize("Read Entrails") == "read-entrails"
    assert normalize("Assassin's Dagger") == "assassins-dagger"
    assert normalize("The Big One") == "big-one"


def test_load():
    c = Compendium.load("base")
    assert c

    assert c.title == 'Troika Numinous Edition'
    assert c.author == 'Daniel Sell'
    assert c.url == 'https://docs.google.com/document/d/1haUfSVekt2gNab3V2CrL1Pg_sZ-ZlskphwXmSnGT9aw/edit'
    assert c.key == 'base'

    assert len(c._backgrounds.keys()) == 36
