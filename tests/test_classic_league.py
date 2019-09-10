import aiohttp

from fpl.models.classic_league import ClassicLeague
from tests.helper import AsyncMock

classic_league_data = {
    "new_entries": {
        "has_next": False,
        "number": 1,
        "results": []
    },
    "league": {
        "id": 633353,
        "leagueban_set": [],
        "name": "Steem Fantasy League",
        "short_name": None,
        "created": "2018-08-07T00:03:18Z",
        "closed": False,
        "forum_disabled": False,
        "make_code_public": False,
        "rank": None,
        "size": None,
        "league_type": "x",
        "_scoring": "c",
        "reprocess_standings": False,
        "admin_entry": 2779525,
        "start_event": 1
    },
    "standings": {
        "has_next": True,
        "page": 1,
        "results": [
            {
                "id": 31124573,
                "entry_name": "awd2",
                "event_total": 82,
                "player_name": "Oleg Smolerov",
                "movement": "same",
                "own_entry": False,
                "rank": 1,
                "last_rank": 1,
                "rank_sort": 1,
                "total": 1677,
                "entry": 123748,
                "league": 633353,
                "start_event": 1,
                "stop_event": 38
            },
            {
                "id": 20990567,
                "entry_name": "Metalheadz",
                "event_total": 58,
                "player_name": "Robert Roman",
                "movement": "same",
                "own_entry": False,
                "rank": 2,
                "last_rank": 2,
                "rank_sort": 2,
                "total": 1634,
                "entry": 3645024,
                "league": 633353,
                "start_event": 1,
                "stop_event": 38
            }
        ]
    },
    "update_status": 0
}


class TestClassicLeague(object):
    async def test_init(self, loop):
        session = aiohttp.ClientSession()
        classic_league = ClassicLeague(classic_league_data, session)
        assert classic_league._session is session
        for k, v in classic_league_data.items():
            assert getattr(classic_league, k) == v
        await session.close()

    async def test_str(self, loop, classic_league):
        assert str(classic_league) == "Steem Fantasy League - 633353"

    async def test_get_standings(self, loop, mocker, classic_league):
        data = {"standings": classic_league_data["standings"]}
        mocked_fetch = mocker.patch("fpl.models.classic_league.fetch",
                                    return_value=data,
                                    new_callable=AsyncMock)
        standings = await classic_league.get_standings(1)
        assert isinstance(standings, dict)
        assert standings["page"] == 1
        assert standings["results"][0]["rank"] == 1
