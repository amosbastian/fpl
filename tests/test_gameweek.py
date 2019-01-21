class TestGameweek(object):
    def test_gameweek(self, loop, gameweek):
        assert gameweek.__str__() == "Gameweek 6 - 22 Sep 11:30"

    def test_fixtures(self, loop, gameweek):
        assert isinstance(gameweek.fixtures, list)
