class TestH2HLeague(object):
    def test_h2h_league(self, loop, h2h_league):
        assert h2h_league.__str__() == "League 760869 - 760869"

    async def test_fixtures(self, loop, h2h_league):
        fixtures = await h2h_league.get_fixtures()
        assert isinstance(fixtures, list)
        assert isinstance(fixtures[0], dict)
