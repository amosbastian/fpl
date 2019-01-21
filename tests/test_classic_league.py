class TestClassicLeague(object):
    async def test_classic_league(self, loop, classic_league):
        assert classic_league.__str__() == "Steem Fantasy League - 633353"

    async def test_get_standings(self, loop, classic_league):
        standings = await classic_league.get_standings(1)
        assert isinstance(standings, dict)
        assert standings["results"][0]["rank"] == 1
