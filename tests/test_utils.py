import aiohttp
import pytest

from fpl.utils import (chip_converter, get_csrf_token, get_current_gameweek,
                       get_headers, logged_in, position_converter,
                       team_converter)


class TestUtils(object):
    async def test_get_current_gameweek(self, loop, fpl):
        with pytest.raises(TypeError):
            current_gameweek = await get_current_gameweek(fpl.session)
        await fpl.login()
        current_gameweek = await get_current_gameweek(fpl.session)
        assert isinstance(current_gameweek, int)

    async def test_team_converter(self, loop, fpl):
        teams = await fpl.get_teams()
        for team in teams:
            assert team_converter(team.id) == team.name

    def test_position_converter(self):
        positions = ["Goalkeeper", "Defender", "Midfielder", "Forward"]
        converted = [position_converter(position) for position in range(1, 5)]
        assert positions == converted

    def test_chip_converter(self):
        chips = ["TC", "WC", "BB", "FH"]
        converted = [chip_converter(chip) for chip in [
            "3xc", "wildcard", "bboost", "freehit"]]

        assert chips == converted

    async def test_logged_in(self, loop, fpl):
        await fpl.login()
        assert logged_in(fpl.session)

    async def test_get_csrf_token(self, loop, fpl):
        with pytest.raises(KeyError):
            await get_csrf_token(fpl.session)
        await fpl.login()
        csrf_token = await get_csrf_token(fpl.session)
        assert isinstance(csrf_token, str)

    def test_get_headers(self):
        headers = get_headers("123", "456")
        assert isinstance(headers, dict)
