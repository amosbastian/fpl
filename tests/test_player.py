import pytest


class TestPlayer:
    @pytest.mark.asyncio
    async def test_games_played(event_loop, player):
        games_played = await player.games_played
        assert isinstance(games_played, int)

        if player.minutes > 0:
            assert games_played > 0

    def test_pp90(event_loop, player):
        pp90 = player.pp90
        assert isinstance(pp90, float)

    @pytest.mark.asyncio
    async def test_vapm(event_loop, player):
        vapm = await player.vapm
        assert isinstance(vapm, float)
