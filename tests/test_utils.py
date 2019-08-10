import pytest

from fpl.utils import (chip_converter, get_current_gameweek, get_headers,
                       logged_in, position_converter, team_converter)


class TestUtils(object):
    async def test_get_current_gameweek(self, loop, fpl):
        current_gameweek = await get_current_gameweek(fpl.session)
        assert isinstance(current_gameweek, int)

    async def test_team_converter(self, loop, fpl):
        teams = await fpl.get_teams()
        for team in teams:
            assert team_converter(team.id) == team.name

    @staticmethod
    def test_position_converter():
        positions = ["Goalkeeper", "Defender", "Midfielder", "Forward"]
        converted = [position_converter(position) for position in range(1, 5)]
        assert positions == converted

    @staticmethod
    def test_chip_converter():
        chips = ["TC", "WC", "BB", "FH"]
        converted = [chip_converter(chip) for chip in [
            "3xc", "wildcard", "bboost", "freehit"]]

        assert chips == converted

    async def test_logged_in(self, loop, fpl):
        await fpl.login()
        assert logged_in(fpl.session)

    @staticmethod
    def test_get_headers():
        headers = get_headers("123")
        assert isinstance(headers, dict)
