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
from datetime import datetime
from .models.classic_league import ClassicLeague
from .models.fixture import Fixture
from .models.gameweek import Gameweek
from .models.h2h_league import H2HLeague
from .models.player import Player
from .models.team import Team
from .models.user import User
from pymongo import MongoClient
from .utils import team_converter, scale, average


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
        response = session.post(login_url, data=payload)

        if "Incorrect email or password" in response.text:
            raise ValueError("Incorrect email or password!")

        self.session = session

    def update_mongodb(self):
        """Updates or creates a MongoDB database with the collection players
        and teams.
        """
        client = MongoClient()
        database = client.fpl

        def update_teams():
            """Updates all teams of the Fantasy Premier League."""
            print("{} - updating teams.".format(datetime.now()))
            database_teams = database.teams
            teams = FPL.get_teams()

            for team in teams:
                team = {k: v for k, v in vars(team).items()
                        if not k.startswith("_")}

                database_teams.replace_one(
                    {"team_id": team["team_id"]}, team, upsert=True)

        def update_players():
            """Updates all players of the Fantasy Premier League."""
            print("{} - updating players.".format(datetime.now()))
            database_players = database.players
            players = FPL.get_players()

            for player in players:
                player = {k: v for k, v in vars(player).items()
                          if not k.startswith("_")}

                database_players.replace_one(
                    {"player_id": player["player_id"]}, player, upsert=True)

        def update_fdr():
            """Updates the FDR of each team in the Fantasy Premier League."""
            print("{} - updating FDR.".format(datetime.now()))
            team_fdr = self.FDR(mongodb=True)
            for team_name, fdr in team_fdr.items():
                team = database.teams.update_one(
                    {"name": team_name}, {"$set": {"FDR": fdr}}, upsert=True)

        def update_fixtures():
            """Updates the fixtures of each team, which includes the FDR of
            that specific fixture.
            """
            print("{} - updating fixtures.".format(datetime.now()))
            for team in database.teams.find():
                # Find one player of each team and use them to get the fixtures
                player = database.players.find_one({"team": team["name"]})
                fixtures = player["fixtures"]
                for fixture in fixtures:
                    location = "H" if fixture["is_home"] else "A"
                    opponent = database.teams.find_one(
                        {"name": fixture["opponent_name"]})
                    fdr = {position: difficulty[location]
                           for position, difficulty in opponent["FDR"].items()}
                    fixture["FDR"] = fdr

                database.teams.update_one({"_id": team["_id"]},
                                          {"$set": {"fixtures": fixtures}},
                                          upsert=True)

        update_teams()
        update_players()
        update_fdr()
        update_fixtures()

    def get_points_against(self, players=None):
        """Returns a dictionary containing the points scored against
        all teams in the Premier League, split by position.
        """
        if not players:
            players = []
            for player in self.get_players():
                players.append({k: v for k, v in vars(player).items()
                               if not k.startswith("_")})

        points_against = {}

        for player in players:
            position = player["position"].lower()
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

    def FDR(self, mongodb=False):
        """Creates a new Fixture Difficulty Ranking (FDR) based on the amount
        of points each team concedes in Fantasy Premier League terms.
        """
        if mongodb:
            client = MongoClient()
            database = client.fpl
            players = database.players.find()
        else:
            players = self.get_players()

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

        points_against = self.get_points_against(players)
        average_points = average_points_against(points_against)
        extrema = get_extrema(average_points)
        fdr = calculate_fdr(average_points, extrema)

        return fdr
