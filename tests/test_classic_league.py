import aiohttp

from fpl.models.classic_league import ClassicLeague


class TestClassicLeague(object):
    async def test_init(self, loop):
        data = {
            "new_entries": {"has_next": False, "number": 1, "results": []},
            "league": {
                "id": 1,
                "leagueban_set": [],
                "name": "Arsenal",
                "short_name": "team-1",
                "created": "2018-07-05T12:12:23Z",
                "closed": False,
            },
        }
        session = aiohttp.ClientSession()
        classic_league = ClassicLeague(data, session)
        assert classic_league._session is session
        for k, v in data.items():
            assert getattr(classic_league, k) == v
        await session.close()

    async def test_classic_league(self, loop, classic_league):
        assert classic_league.__str__() == "Steem Fantasy League - 633353"

    async def test_get_standings(self, loop, classic_league):
        standings = await classic_league.get_standings(1)
        assert isinstance(standings, dict)
        assert standings["results"][0]["rank"] == 1
