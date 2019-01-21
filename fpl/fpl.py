"""
The FPL module.

Fantasy Premier League API:
* /bootstrap-static
* /bootstrap-dynamic
* /elements
* /element-summary/{player_id}
* /entry/{user_id}
* /entry/{user_id}/cup
* /entry/{user_id}/event/{event_id}/picks
* /entry/{user_id}/history
* /entry/{user_id}/transfers
* /events
* /event/{event_id}/live
* /fixtures/?event={event_id}
* /game-settings
* /leagues-classic-standings/{league_id}
* /leagues-classic-standings/{league_id}
* /leagues-entries-and-h2h-matches/league/{league_id}
* /leagues-h2h-standings/{league_id}
* /my-team/{user_id}
* /teams
* /transfers
"""
import asyncio
import itertools
import os
from datetime import datetime

import aiohttp

from .constants import API_URLS
from .models.classic_league import ClassicLeague
from .models.fixture import Fixture
from .models.gameweek import Gameweek
from .models.h2h_league import H2HLeague
from .models.player import Player, PlayerSummary
from .models.team import Team
from .models.user import User
from .utils import average, fetch, position_converter, scale, team_converter


class FPL():
    """The FPL class."""
    def __init__(self, session):
        self.session = session

    async def get_user(self, user_id, return_json=False):
        """Returns a `User` object or JSON containing information about the
        user with the given `user_id`.

        :param string user_id: A user's id
        :param boolean return_json: return dict if True, otherwise User
        """
        url = API_URLS["user"].format(user_id)
        user = await fetch(self.session, url)

        if return_json:
            return user
        return User(user, session=self.session)

    async def get_teams(self, team_ids=[], return_json=False):
        """Returns a list JSON or `Team` objects of the teams currently
        participating in the Premier League.

        :param list team_ids: List containing the IDs of desired teams
        :param boolean return_json: return dict if True, otherwise Team
        """
        url = API_URLS["teams"]
        teams = await fetch(self.session, url)

        if team_ids:
            teams = [team for team in teams if team["id"] in team_ids]

        if return_json:
            return teams

        return [Team(team_information, self.session)
                for team_information in teams]

    async def get_team(self, team_id, return_json=False):
        """Returns a `Team` object or JSON containing information about the
        team with the given `team_id`.

        :param int team_id: A team's id
        :param boolean return_json: return dict if True, otherwise Player

        .. code-block:: none

             1 - Arsenal
             2 - Bournemouth
             3 - Brighton
             4 - Burnley
             5 - Cardiff
             6 - Chelsea
             7 - Crystal Palace
             8 - Everton
             9 - Fulham
            10 - Huddersfield
            11 - Leicester
            12 - Liverpool
            13 - Man City
            14 - Man Utd
            15 - Newcastle
            16 - Southampton
            17 - Spurs
            18 - Watford
            19 - West Ham
            20 - Wolves
        """
        url = API_URLS["teams"]
        teams = await fetch(self.session, url)

        if return_json:
            return teams[team_id + 1]

        return Team(teams[team_id + 1], self.session)

    async def get_player_summary(self, player_id, return_json=False):
        """Returns a `PlayerSummary` or JSON object with the given `player_id`

        :param int player_id: A player's ID
        :param boolean return_json: return dict if True, otherwise Player
        """
        url = API_URLS["player"].format(player_id)
        player_summary = await fetch(self.session, url)

        if return_json:
            return player_summary

        return PlayerSummary(player_summary)

    async def get_player_summaries(self, player_ids=[], return_json=False):
        """Returns a list of `PlayerSummary` or JSON objects with the given
        `player_ids`

        :param list player_ids: A list of player IDs
        :param boolean return_json: return dict if True, otherwise Player
        """
        tasks = [asyncio.ensure_future(
                 fetch(self.session, API_URLS["player"].format(player_id)))
                 for player_id in player_ids]

        player_summaries = await asyncio.gather(*tasks)

        if return_json:
            return player_summaries

        return [PlayerSummary(player_summary)
                for player_summary in player_summaries]

    async def get_player(self, player_id, players=None, include_summary=False,
                         return_json=False):
        """Returns a `Player` or JSON object with the given `player_id`.

        :param int player_id: A player's ID
        :param list players: A list of players
        :param boolean include_summary: include player's summary if True
        :param boolean return_json: return dict if True, otherwise Player
        """
        if not players:
            players = await fetch(self.session, API_URLS["players"])

        player = next(player for player in players
                      if player["id"] == player_id)

        if include_summary:
            player_summary = await self.get_player_summary(
                player["id"], return_json=True)
            player.update(player_summary)

        if return_json:
            return player

        return Player(player)

    async def get_players(self, player_ids=[], include_summary=False,
                          return_json=False):
        """Returns a list of `Player` or JSON objects of either all players or
        players with the given IDs.

        :param list player_ids: A list of player IDs
        :param boolean include_summary: include player's summary if True
        :param boolean return_json: return dict if True, otherwise Player
        """
        players = await fetch(self.session, API_URLS["players"])
        if not player_ids:
            player_ids = [player["id"] for player in players]

        tasks = [asyncio.ensure_future(
                 self.get_player(
                     player_id, players, include_summary, return_json))
                 for player_id in player_ids]
        players = await asyncio.gather(*tasks)

        return players

    async def get_fixture(self, fixture_id, return_json=False):
        """Returns the fixture with the given `fixture_id`.

        :param int fixture_id: The fixture's ID
        :param boolean return_json: return dict if True, otherwise Fixture
        """
        fixtures = await fetch(self.session, API_URLS["fixtures"])

        fixture = next(fixture for fixture in fixtures
                       if fixture["id"] == fixture_id)
        fixture_gameweek = fixture["event"]

        gameweek_fixtures = await fetch(
            self.session,
            API_URLS["gameweek_fixtures"].format(fixture_gameweek))

        fixture = next(fixture for fixture in gameweek_fixtures
                       if fixture["id"] == fixture_id)

        if return_json:
            return fixture

        return Fixture(fixture)

    async def get_fixtures_by_id(self, fixture_ids, return_json=False):
        """Returns a list of all fixtures with IDs included in the
        `fixture_ids` list.

        :param list fixture_ids: A list of fixture IDs
        :param boolean return_json: return dict if True, otherwise Fixture
        """
        fixtures = await fetch(self.session, API_URLS["fixtures"])
        fixture_gameweeks = set(fixture["event"] for fixture in fixtures
                                if fixture["id"] in fixture_ids)
        tasks = [asyncio.ensure_future(
                 fetch(self.session,
                       API_URLS["gameweek_fixtures"].format(gameweek)))
                 for gameweek in fixture_gameweeks]

        gameweek_fixtures = await asyncio.gather(*tasks)
        merged_fixtures = list(itertools.chain(*gameweek_fixtures))

        fixtures = [fixture for fixture in merged_fixtures
                    if fixture["id"] in fixture_ids]

        if return_json:
            return fixtures

        return [Fixture(fixture) for fixture in fixtures]

    async def get_fixtures_by_gameweek(self, gameweek, return_json=False):
        """Returns a list of all fixtures of a given gameweek.

        :param int gameweek: A gameweek
        :param boolean return_json: return dict if True, otherwise Fixture
        """
        fixtures = await fetch(self.session,
                               API_URLS["gameweek_fixtures"].format(gameweek))

        if return_json:
            return fixtures

        return [Fixture(fixture) for fixture in fixtures]

    async def get_fixtures(self, return_json=False):
        """Returns a list of all fixtures.

        :param list fixture_ids: A list of fixture IDs
        :param boolean return_json: return dict if True, otherwise Fixture
        """
        gameweeks = range(1, 39)
        tasks = [asyncio.ensure_future(
                 fetch(self.session,
                       API_URLS["gameweek_fixtures"].format(gameweek)))
                 for gameweek in gameweeks]

        gameweek_fixtures = await asyncio.gather(*tasks)
        fixtures = list(itertools.chain(*gameweek_fixtures))

        if return_json:
            return fixtures

        return [Fixture(fixture) for fixture in fixtures]

    async def get_gameweek(self, gameweek_id, include_live=False,
                           return_json=False):
        """Returns a `Gameweek` or JSON object of the specified gameweek.

        :param int gameweek_id: A gameweek's id
        :param boolean return_json: return dict if True, otherwise Gameweek
        """

        static_gameweeks = await fetch(self.session, API_URLS["gameweeks"])
        static_gameweek = next(gameweek for gameweek in static_gameweeks if
                               gameweek["id"] == gameweek_id)
        live_gameweek = await fetch(
            self.session, API_URLS["gameweek_live"].format(gameweek_id))

        live_gameweek.update(static_gameweek)

        if return_json:
            return live_gameweek

        return Gameweek(live_gameweek)

    async def get_gameweeks(self, gameweek_ids=[], include_live=False,
                            return_json=False):
        """Returns a list `Gameweek` or JSON objects of either all gameweeks
        or the gameweeks with the given IDs.

        :param list gameweek_ids: A list of gameweek IDs
        :param boolean return_json: return dict if True, otherwise Gameweek
        """

        if not gameweek_ids:
            gameweek_ids = range(1, 39)

        tasks = [asyncio.ensure_future(
                 self.get_gameweek(gameweek_id, include_live, return_json))
                 for gameweek_id in gameweek_ids]

        gameweeks = await asyncio.gather(*tasks)
        return gameweeks

    async def game_settings(self):
        """Returns a dictionary containing the Fantasy Premier League's rules.
        """
        settings = await fetch(self.session, API_URLS["settings"])
        return settings

    async def get_classic_league(self, league_id, return_json=False):
        """Returns a `ClassicLeague` or JSON  object with the given
        `league_id`.

        :param string league_id: A league's id
        :param boolean return_json: return dict if True, otherwise ClassicLeague
        """
        url = API_URLS["league_classic"].format(league_id)
        league = await fetch(self.session, url)

        if return_json:
            return league

        return ClassicLeague(league, session=self.session)

    async def get_h2h_league(self, league_id, return_json=False):
        """Returns a `H2HLeague` object with the given `league_id`.

        :param string league_id: A league's id
        :param boolean return_json: return dict if True, otherwise H2HLeague
        """
        url = API_URLS["league_h2h"].format(league_id)
        league = await fetch(self.session, url)

        if return_json:
            return league

        return H2HLeague(league, session=self.session)

    async def login(self, email=None, password=None):
        """Returns a requests session with FPL login authentication.

        :param string user: email
        :param string password: password
        """
        if not email and not password:
            email = os.environ["FPL_EMAIL"]
            password = os.environ["FPL_PASSWORD"]

        url = "https://fantasy.premierleague.com/"
        await self.session.get(url)
        filtered = self.session.cookie_jar.filter_cookies(url)
        assert filtered["csrftoken"]
        csrf_token = filtered["csrftoken"].value

        payload = {
            "csrfmiddlewaretoken": csrf_token,
            "login": email,
            "password": password,
            "app": "plfpl-web",
            "redirect_uri": "https://fantasy.premierleague.com/a/login"
        }

        login_url = "https://users.premierleague.com/accounts/login/"
        async with self.session.post(login_url, data=payload) as response:
            response_text = await response.text()
            if "Incorrect email or password" in response_text:
                raise ValueError("Incorrect email or password!")

    async def get_points_against(self):
        """Returns a dictionary containing the points scored against
        all teams in the Premier League, split by position.
        """
        players = await self.get_players(
            include_summary=True, return_json=True)
        points_against = {}

        for player in players:
            position = position_converter(player["element_type"]).lower()

            for fixture in player["history"]:
                if fixture["minutes"] == 0:
                    continue

                points = fixture["total_points"]
                opponent = team_converter(fixture["opponent_team"])
                location = "H" if fixture["was_home"] else "A"

                points_against.setdefault(
                    opponent,
                    {
                        "all": {"H": [], "A": []},
                        "goalkeeper": {"H": [], "A": []},
                        "defender": {"H": [], "A": []},
                        "midfielder": {"H": [], "A": []},
                        "forward": {"H": [], "A": []}
                    }
                )

                points_against[opponent]["all"][location].append(points)
                points_against[opponent][position][location].append(points)

        return points_against

    async def FDR(self):
        """Creates a new Fixture Difficulty Ranking (FDR) based on the amount
        of points each team concedes in Fantasy Premier League terms.
        """
        def average_points_against(points_against):
            """Averages the points scored against all teams per position."""
            for team, positions in points_against.items():
                for position in positions.values():
                    position["H"] = average(position["H"])
                    position["A"] = average(position["A"])

                points_against[team] = positions

            return points_against

        def get_extrema(points_against):
            """Returns the extrema for each position and location."""
            averages = {}
            for team, positions in points_against.items():
                for position, average in positions.items():
                    averages.setdefault(position, {"H": [], "A": []})
                    averages[position]["H"].append(average["H"])
                    averages[position]["A"].append(average["A"])

            for position, locations in averages.items():
                min_h = min(locations["H"])
                min_a = min(locations["A"])
                max_h = max(locations["H"])
                max_a = max(locations["A"])
                averages[position]["H"] = [min_h, max_h]
                averages[position]["A"] = [min_a, max_a]

            return averages

        def calculate_fdr(average_points, extrema):
            """Returns a dictionary containing the FDR for each team, which is
            calculated by scaling the average points conceded per position
            between 1.0 and 5.0 using the given extrema.
            """
            for team, positions in average_points.items():
                for position, locations in positions.items():
                    min_h, max_h = extrema[position]["H"]
                    min_a, max_a = extrema[position]["A"]

                    fdr_h = scale(locations["H"], 5.0, 1.0, min_h, max_h)
                    fdr_a = scale(locations["A"], 5.0, 1.0, min_a, max_a)

                    average_points[team][position]["H"] = fdr_h
                    average_points[team][position]["A"] = fdr_a

            return average_points

        points_against = await self.get_points_against()
        average_points = average_points_against(points_against)
        extrema = get_extrema(average_points)
        fdr = calculate_fdr(average_points, extrema)

        return fdr

    async def _close(self):
        await self.session.lose()
