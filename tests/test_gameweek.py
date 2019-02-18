class TestGameweek(object):
    @staticmethod
    def test_gameweek(loop, gameweek):
        assert gameweek.__str__() == "Gameweek 6 - 22 Sep 11:30"

    @staticmethod
    def test_fixtures(loop, gameweek):
        assert isinstance(gameweek.fixtures, list)
