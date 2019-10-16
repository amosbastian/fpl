import aiohttp
import pytest

from fpl.models.h2h_league import H2HLeague
from tests.helper import AsyncMock

h2h_league_data = {
   "league": {
      "id": 902521,
      "name": "League of Gentlemen H2H",
      "created": "2019-08-07T12:26:59.153290Z",
      "closed": True,
      "max_entries": 10,
      "league_type": "x",
      "scoring": "h",
      "admin_entry": 114569,
      "start_event": 1,
      "code_privacy": "l",
      "ko_rounds": 2
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
      "results": [
         {
            "id": 1310429,
            "division": 117276,
            "entry": 737174,
            "player_name": "Mark Nicholson",
            "rank": 1,
            "last_rank": 1,
            "rank_sort": 1,
            "total": 18,
            "entry_name": "Nico",
            "matches_played": 8,
            "matches_won": 6,
            "matches_drawn": 0,
            "matches_lost": 2,
            "points_for": 422
         },
         {
            "id": 1310426,
            "division": 117276,
            "entry": 114569,
            "player_name": "John Madden",
            "rank": 2,
            "last_rank": 3,
            "rank_sort": 2,
            "total": 15,
            "entry_name": "The Dead Eye Dicks",
            "matches_played": 8,
            "matches_won": 5,
            "matches_drawn": 0,
            "matches_lost": 3,
            "points_for": 463
         },
         {
            "id": 1310433,
            "division": 117276,
            "entry": 902573,
            "player_name": "Darragh Murphy",
            "rank": 2,
            "last_rank": 2,
            "rank_sort": 3,
            "total": 15,
            "entry_name": "Bop Bop Baby FC",
            "matches_played": 8,
            "matches_won": 5,
            "matches_drawn": 0,
            "matches_lost": 3,
            "points_for": 463
         },
         {
            "id": 1310427,
            "division": 117276,
            "entry": 1263266,
            "player_name": "Matthew Gannon",
            "rank": 4,
            "last_rank": 5,
            "rank_sort": 4,
            "total": 15,
            "entry_name": "The Dead Ends",
            "matches_played": 8,
            "matches_won": 5,
            "matches_drawn": 0,
            "matches_lost": 3,
            "points_for": 420
         },
         {
            "id": 1310428,
            "division": 117276,
            "entry": 3915880,
            "player_name": "Mark Cashin",
            "rank": 5,
            "last_rank": 4,
            "rank_sort": 5,
            "total": 12,
            "entry_name": "Tadhger Roll FC",
            "matches_played": 8,
            "matches_won": 4,
            "matches_drawn": 0,
            "matches_lost": 4,
            "points_for": 410
         },
         {
            "id": 1310430,
            "division": 117276,
            "entry": 4192950,
            "player_name": "Brian Doyle",
            "rank": 6,
            "last_rank": 6,
            "rank_sort": 6,
            "total": 12,
            "entry_name": "#",
            "matches_played": 8,
            "matches_won": 4,
            "matches_drawn": 0,
            "matches_lost": 4,
            "points_for": 394
         },
         {
            "id": 1310431,
            "division": 117276,
            "entry": 4276671,
            "player_name": "Paraic O'Keeffe",
            "rank": 7,
            "last_rank": 7,
            "rank_sort": 7,
            "total": 9,
            "entry_name": "Celso FC",
            "matches_played": 8,
            "matches_won": 3,
            "matches_drawn": 0,
            "matches_lost": 5,
            "points_for": 413
         },
         {
            "id": 1310435,
            "division": 117276,
            "entry": 4378761,
            "player_name": "Martin Dunphy",
            "rank": 8,
            "last_rank": 8,
            "rank_sort": 8,
            "total": 9,
            "entry_name": "No, Money Down FC",
            "matches_played": 8,
            "matches_won": 3,
            "matches_drawn": 0,
            "matches_lost": 5,
            "points_for": 404
         },
         {
            "id": 1310434,
            "division": 117276,
            "entry": 3954777,
            "player_name": "jimmy murphy",
            "rank": 9,
            "last_rank": 9,
            "rank_sort": 9,
            "total": 9,
            "entry_name": "Cows United",
            "matches_played": 8,
            "matches_won": 3,
            "matches_drawn": 0,
            "matches_lost": 5,
            "points_for": 400
         },
         {
            "id": 1310432,
            "division": 117276,
            "entry": 3860719,
            "player_name": "Richard O Shea",
            "rank": 10,
            "last_rank": 10,
            "rank_sort": 10,
            "total": 6,
            "entry_name": "Sampras",
            "matches_played": 8,
            "matches_won": 2,
            "matches_drawn": 0,
            "matches_lost": 6,
            "points_for": 417
         }
      ]
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
        assert h2h_league.__str__() == "League of Gentlemen H2H - 902521"

    async def test_get_fixtures_with_known_gameweek_unauthorized(
            self, loop, h2h_league):
        with pytest.raises(Exception):
            await h2h_league.get_fixtures(1)

    async def test_get_fixtures_with_known_gameweek_authorized(  # issue with login
            self, loop, mocker, h2h_league):
        mocked_logged_in = mocker.patch(
            "fpl.models.h2h_league.logged_in", return_value=True)
        mocked_fetch = mocker.patch(
            "fpl.models.h2h_league.fetch", return_value={}, new_callable=AsyncMock)
        fixtures = await h2h_league.get_fixtures(gameweek=1)
        assert isinstance(fixtures, list)
        assert len(fixtures) == 5
        mocked_logged_in.assert_called_once()
        mocked_fetch.assert_called_once()

    async def test_get_fixtures_with_unknown_gameweek_unauthorized(
            self, loop, h2h_league):
        with pytest.raises(Exception):
            await h2h_league.get_fixtures()

    async def test_get_fixtures_with_unknown_gameweek_authorized(  # issue with login
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

    # async def test_get_full_standings(
    #         self, loop, mocker, h2h_league):
    #     mocked_logged_in = mocker.patch(
    #         "fpl.models.h2h_league.logged_in", return_value=True)
    #     mocked_fetch = mocker.patch(
    #         "fpl.models.h2h_league.fetch", return_value={}, new_callable=AsyncMock)
    #     standings = await h2h_league.get_full_standings()
    #     assert isinstance(standings["results"], list)
    #     mocked_logged_in.assert_called_once()
    #     mocked_fetch.assert_called_once()
