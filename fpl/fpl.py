import requests
import json
from .user import User
from .team import Team
from .player import Player
from .gameweek import Gameweek
from .h2h_league import H2HLeague
from .classic_league import ClassicLeague


API_BASE_URL = "https://fantasy.premierleague.com/drf/"


class FPL():
    def get_user(self, user_id):
        """
        Returns a `User` object containing information about the user with the
        given `user_id`.

        :param string user_id: A user's id
        """
        return User(user_id)

    def get_teams(self):
        """
        Returns a list of `Team` objects of the teams currently participating
        in the Premier League.
        """
        return[Team(team_id) for team_id in range(1, 21)]

    def get_team(self, team_id):
        """
        Returns a `Team` object containing information about the team with the
        given `team_id`.

        :param string user_id: A team's id

        .. code-block:: none

             1 - Arsenal
             2 - Bournemouth
             3 - Brighton
             4 - Burnley
             5 - Chelsea
             6 - Crystal Palace
             7 - Everton
             8 - Huddersfield
             9 - Leicester
            10 - Liverpool
            11 - Man City
            12 - Man Utd
            13 - Newcastle
            14 - Southampton
            15 - Stoke
            16 - Swansea
            17 - Spurs
            18 - Watford
            19 - West Brom
        """
        return Team(team_id)

    def get_players(self):
        """
        Returns a list of `Player` objects of all players currently playing for
        teams in the Premier League.
        """
        players = []
        response = requests.get("{}elements".format(API_BASE_URL))
        if response.status_code == 200:
            for player in response.json():
                players.append(Player(player["id"], player))
        else:
            print("Something went wrong, please try again later...")
            return []
        return players

    def get_gameweeks(self):
        """
        Returns a list `Gameweek` objects.
        """
        return [Gameweek(gameweek_id) for gameweek_id in range(1, 38)]

    def get_gameweek(self, gameweek_id):
        """
        Returns a `Gameweek` object of the specified gameweek.

        :param int gameweek: The gameweek (1-38)
        """
        return Gameweek(gameweek_id)

    def game_settings(self):
        """
        Returns a dictionary containing the Fantasy Premier League's rules.
        """
        return requests.get("{}game-settings".format(API_BASE_URL)).json()

    def get_classic_league(self, league_id):
        """
        Returns a `ClassicLeague` object with the given `league_id`.

        :param string league_id: A league's id
        """
        return ClassicLeague(league_id)

    def get_h2h_league(self, league_id):
        """
        Returns a `H2HLeague` object with the given `league_id`.

        :param string league_id: A league's id
        """
        return H2HLeague(league_id)
