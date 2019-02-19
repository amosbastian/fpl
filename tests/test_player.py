class TestPlayer(object):
    @staticmethod
    def test_games_played(loop, player):
        games_played = player.games_played
        assert isinstance(games_played, int)

    @staticmethod
    def test_pp90(loop, player):
        pp90 = player.pp90
        assert isinstance(pp90, float)
