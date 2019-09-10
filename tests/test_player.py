class TestPlayer(object):
    @staticmethod
    async def test_games_played(loop, player):
        games_played = await player.games_played
        assert isinstance(games_played, int)

        if player.minutes > 0:
            assert games_played > 0

    @staticmethod
    def test_pp90(loop, player):
        pp90 = player.pp90
        assert isinstance(pp90, float)

    @staticmethod
    async def test_vapm(loop, player):
        vapm = await player.vapm
        assert isinstance(vapm, float)
