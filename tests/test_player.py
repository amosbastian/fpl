class TestPlayer(object):
    def test_games_played(self, loop, player):
        games_played = player.games_played
        assert isinstance(games_played, int)

    def test_pp90(self, loop, player):
        pp90 = player.pp90
        assert isinstance(pp90, float)
