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
import os
import requests

from .constants import API_URLS
from fpl.models import *


class FPL():
    """The FPL class."""
    def __init__(self):
        self.session = None

    def get_user(self, user_id):
        """Returns a `User` object containing information about the user with
        the given `user_id`.

        :param string user_id: A user's id
        """
        return User(user_id, session=self.session)

    @staticmethod
    def get_teams():
        """Returns a list of `Team` objects of the teams currently
        participating in the Premier League.
        """
        return[Team(team_id) for team_id in range(1, 21)]

    @staticmethod
    def get_team(team_id):
        """Returns a `Team` object containing information about the team with
        the given `team_id`.

        :param int team_id: A team's id

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
        return Team(team_id)

    @staticmethod
    def get_player(player_id):
        """Returns the `Player` object with the given `player_id`.

        :param int player_id: A player's ID
        """
        return Player(player_id, additional=None)

    @staticmethod
    def get_players(player_ids=None):
        """Returns a list of `Player` objects of all players currently playing
        for teams in the Premier League.
        """
        if not player_ids:
            player_ids = range(0, 600)
        players = []
        response = requests.get(API_URLS["players"])
        if response.status_code == 200:
            for player in response.json():
                if player["id"] in player_ids:
                    players.append(Player(player["id"], player))
        else:
            print("Something went wrong, please try again later...")
            return []
        return players

    @staticmethod
    def get_fixture(fixture_id, gameweek=None):
        """Returns the fixture with the given ID."""
        if gameweek:
            response = requests.get(API_URLS["gameweek_fixtures"].format(
                gameweek)).json()
        else:
            response = requests.get(API_URLS["fixtures"]).json()

        for fixture in response:
            if fixture["id"] == fixture_id:
                return Fixture(fixture)
        return []

    @staticmethod
    def get_fixtures(gameweek=None):
        """Returns all possible fixtures, or all fixtures of a specific
        gameweek.
        """
        if gameweek:
            response = requests.get(API_URLS["gameweek_fixtures"].format(
                gameweek)).json()
        else:
            response = requests.get(API_URLS["fixtures"]).json()

        return [Fixture(fixture) for fixture in response]

    @staticmethod
    def get_gameweeks():
        """Returns a list `Gameweek` objects."""
        return [Gameweek(gameweek_id) for gameweek_id in range(1, 39)]

    @staticmethod
    def get_gameweek(gameweek_id):
        """Returns a `Gameweek` object of the specified gameweek.

        :param int gameweek_id: A gameweek's id.
        """
        return Gameweek(gameweek_id)

    @staticmethod
    def game_settings():
        """Returns a dictionary containing the Fantasy Premier League's rules.
        """
        return requests.get(API_URLS["settings"]).json()

    @staticmethod
    def get_classic_league(league_id):
        """Returns a `ClassicLeague` object with the given `league_id`.

        :param string league_id: A league's id
        """
        return ClassicLeague(league_id)

    def get_h2h_league(self, league_id):
        """Returns a `H2HLeague` object with the given `league_id`.

        :param string league_id: A league's id
        """
        return H2HLeague(league_id, session=self.session)

    def login(self, email=None, password=None):
        """Returns a requests session with FPL login authentication.

        :param string user: email
        :param string password: password
        """
        if not email and not password:
            email = os.environ["FPL_EMAIL"]
            password = os.environ["FPL_PASSWORD"]

        session = requests.Session()

        session.get("https://fantasy.premierleague.com/")
        csrftoken = session.cookies["csrftoken"]

        payload = {
            "csrfmiddlewaretoken": csrftoken,
            "login": email,
            "password": password,
            "app": "plfpl-web",
            "redirect_uri": "https://fantasy.premierleague.com/a/login"
        }

        login_url = "https://users.premierleague.com/accounts/login/"
        session.post(login_url, data=payload)

        self.session = session
