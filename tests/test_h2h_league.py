import aiohttp
import pytest

from fpl.models.h2h_league import H2HLeague
from tests.helper import AsyncMock

h2h_league_data = {
    "new_entries": {"has_next": False, "number": 1, "results": []},
    "league": {
        "id": 829116,
        "leagueban_set": [],
        "name": "League 829116",
        "has_started": True,
        "can_delete": False,
        "short_name": None,
        "created": "2018-08-09T18:10:37Z",
        "closed": True,
        "forum_disabled": False,
        "make_code_public": False,
        "rank": None,
        "size": None,
        "league_type": "c",
        "_scoring": "h",
        "ko_rounds": 2,
        "admin_entry": None,
        "start_event": 1,
    },
    "standings": {"has_next": False, "number": 1, "results": []},
    "matches_next": {},
    "matches_this": {},
}


class TestH2HLeague(object):
    async def test_init(self, loop):
        session = aiohttp.ClientSession()
        league = H2HLeague(h2h_league_data, session)
        assert league._session == session
        for k, v in h2h_league_data.items():
            assert getattr(league, k) == v
        await session.close()

    @staticmethod
    def test_h2h_league(loop, h2h_league):
        assert h2h_league.__str__() == "League 829116 - 829116"

    async def test_get_fixtures_with_known_gameweek_unauthorized(
            self, loop, h2h_league):
        with pytest.raises(Exception):
            await h2h_league.get_fixtures(1)

    async def test_get_fixtures_with_known_gameweek_authorized(
            self, loop, mocker, h2h_league):
        mocked_logged_in = mocker.patch(
            "fpl.models.h2h_league.logged_in", return_value=True)
        mocked_fetch = mocker.patch(
            "fpl.models.h2h_league.fetch", return_value={}, new_callable=AsyncMock)
        fixtures = await h2h_league.get_fixtures(1)
        assert isinstance(fixtures, list)
        assert len(fixtures) == 1
        mocked_logged_in.assert_called_once()
        mocked_fetch.assert_called_once()

    async def test_get_fixtures_with_unknown_gameweek_unauthorized(
            self, loop, h2h_league):
        with pytest.raises(Exception):
            await h2h_league.get_fixtures()

    async def test_get_fixtures_with_unknown_gameweek_authorized(
            self, loop, mocker, h2h_league):
        mocked_logged_in = mocker.patch(
            "fpl.models.h2h_league.logged_in", return_value=True)
        mocked_fetch = mocker.patch(
            "fpl.models.h2h_league.fetch", return_value={}, new_callable=AsyncMock)
        gameweek_number = 3
        mocked_current_gameweek = mocker.patch(
            "fpl.models.h2h_league.get_current_gameweek",
            return_value=gameweek_number,
            new_callable=AsyncMock)
        fixtures = await h2h_league.get_fixtures()
        assert isinstance(fixtures, list)
        assert len(fixtures) == gameweek_number
        assert mocked_fetch.call_count == gameweek_number
        mocked_logged_in.assert_called_once()
        mocked_current_gameweek.assert_called_once()
