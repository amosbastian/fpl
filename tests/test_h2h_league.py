import aiohttp
import pytest

from fpl.models.h2h_league import H2HLeague
from tests.helper import AsyncMock

h2h_league_data = {
    "league": {
        "id": 946125,
        "name": "THE PUNDITS H2H",
        "created": "2019-08-07T20:52:58.751814Z",
        "closed": True,
        "max_entries": None,
        "league_type": "x",
        "scoring": "h",
        "admin_entry": 1726046,
        "start_event": 1,
        "code_privacy": "p",
        "ko_rounds": None
    },
    "new_entries": {
        "has_next": False,
        "page": 1,
        "results": [

        ]
    },
    "standings": {
        "has_next": False,
        "page": 1,
        "results": []
    }
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
        assert h2h_league.__str__() == "THE PUNDITS H2H - 946125"

    async def test_get_fixtures_with_known_gameweek_unauthorized(
            self, loop, h2h_league):
        with pytest.raises(Exception):
            await h2h_league.get_fixtures(gameweek=1)

    @pytest.mark.skip(reason="Need to mock logging in properly.")
    async def test_get_fixtures_with_known_gameweek_authorized(
            self, loop, mocker, fpl, h2h_league):
        mocked_logged_in = mocker.patch(
            "fpl.models.h2h_league.logged_in", return_value=True)

        fixtures = await h2h_league.get_fixtures(gameweek=1)
        assert isinstance(fixtures, list)
        mocked_logged_in.assert_called_once()

    async def test_get_fixtures_with_unknown_gameweek_unauthorized(
            self, loop, h2h_league):
        with pytest.raises(Exception):
            await h2h_league.get_fixtures()

    @pytest.mark.skip(reason="Need to mock logging in properly.")
    async def test_get_fixtures_with_unknown_gameweek_authorized(
            self, loop, mocker, fpl, h2h_league):
        mocked_logged_in = mocker.patch(
            "fpl.models.h2h_league.logged_in", return_value=True)
        await fpl.login()
        fixtures = await h2h_league.get_fixtures()
        assert isinstance(fixtures, list)
        mocked_logged_in.assert_called_once()
