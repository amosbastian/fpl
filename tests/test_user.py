class TestUser(object):
    async def test_gameweek_history(self, loop, user):
        history = await user.get_gameweek_history()
        assert isinstance(history, list)

        history = await user.get_gameweek_history(1)
        assert isinstance(history, dict)

    async def test_season_history(self, loop, user):
        season_history = await user.get_season_history()
        assert isinstance(season_history, list)

    async def test_chips_history(self, loop, user):
        chips = await user.get_chips_history()
        assert isinstance(chips, list)

    async def test_leagues(self, loop, user):
        leagues = user.leagues
        assert isinstance(leagues, dict)

    async def test_picks(self, loop, user):
        picks = await user.get_picks()
        assert isinstance(picks, list)
        assert len(picks) == user.current_event

        picks = await user.get_picks(1)
        assert isinstance(picks, list)

    async def test_active_chips(self, loop, user):
        active_chips = await user.get_active_chips()
        assert isinstance(active_chips, list)
        assert len(active_chips) == user.current_event

        active_chips = await user.get_active_chips(1)
        assert isinstance(active_chips, list)

    async def test_automatic_substitutions(self, loop, user):
        automatic_substitutions = await user.get_automatic_substitutions()
        assert isinstance(automatic_substitutions, list)
        assert len(automatic_substitutions) == user.current_event

        automatic_substitutions = await user.get_automatic_substitutions(1)
        assert isinstance(automatic_substitutions, list)

    async def test_team(self, loop, user):
        team = await user.get_team()
        assert isinstance(team, list)

    async def test_transfers(self, loop, user):
        transfers = await user.get_transfers()
        assert isinstance(transfers, list)

        transfers = await user.get_transfers(1)
        assert isinstance(transfers, list)

    async def test_wildcards(self, loop, user):
        wildcards = await user.get_wildcards()
        assert isinstance(wildcards, list)

    async def test_watchlist(self, loop, user):
        watchlist = await user.get_watchlist()
        assert isinstance(watchlist, list)
