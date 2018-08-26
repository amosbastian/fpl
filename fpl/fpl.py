"""
The FPL module.

Fantasy Premier League API:
* https://fantasy.premierleague.com/drf/bootstrap-static
* https://fantasy.premierleague.com/drf/bootstrap-dynamic
* https://fantasy.premierleague.com/drf/entry/{user_id}
* https://fantasy.premierleague.com/drf/entry/{user_id}/cup
* https://fantasy.premierleague.com/drf/entry/{user_id}/event/{event_id}/picks
* https://fantasy.premierleague.com/drf/entry/{user_id}/history
* https://fantasy.premierleague.com/drf/entry/{user_id}/transfers
* https://fantasy.premierleague.com/drf/elements
* https://fantasy.premierleague.com/drf/element-summary/{player_id}
* https://fantasy.premierleague.com/drf/events
* https://fantasy.premierleague.com/drf/event/{event_id}/live
* https://fantasy.premierleague.com/drf/fixtures/?event={event_id}
* https://fantasy.premierleague.com/drf/game-settings
* https://fantasy.premierleague.com/drf/my-team/{user_id}
* https://fantasy.premierleague.com/drf/teams
* https://fantasy.premierleague.com/drf/transfers
* https://fantasy.premierleague.com/drf/leagues-classic-standings/{league_id}
"""
import requests

from .constants import PLAYER_URL, PLAYERS_URL, GAME_SETTINGS_URL
from .models.classic_league import ClassicLeague
from .models.gameweek import Gameweek
from .models.h2h_league import H2HLeague
from .models.player import Player
from .models.team import Team
from .models.user import User


class FPL():
    """
    The FPL class.
    """
    @staticmethod
    def get_user(user_id):
        """
        Returns a `User` object containing information about the user with the
        given `user_id`.

        :param string user_id: A user's id
        """
        return User(user_id)

    @staticmethod
    def get_teams():
        """
        Returns a list of `Team` objects of the teams currently participating
        in the Premier League.
        """
        return[Team(team_id) for team_id in range(1, 21)]

    @staticmethod
    def get_team(team_id):
        """
        Returns a `Team` object containing information about the team with the
        given `team_id`.

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
        """
        Returns the `Player` object with the given `player_id`.

        :param int player_id: A player's id
        """
        response = requests.get(PLAYER_URL.format(player_id))
        if response.status_code == 200:
            return Player()

    @staticmethod
    def get_players():
        """
        Returns a list of `Player` objects of all players currently playing for
        teams in the Premier League.
        """
        players = []
        response = requests.get(PLAYERS_URL)
        if response.status_code == 200:
            for player in response.json():
                players.append(Player(player["id"], player))
        else:
            print("Something went wrong, please try again later...")
            return []
        return players

    @staticmethod
    def get_gameweeks():
        """
        Returns a list `Gameweek` objects.
        """
        return [Gameweek(gameweek_id) for gameweek_id in range(1, 39)]

    @staticmethod
    def get_gameweek(gameweek_id):
        """
        Returns a `Gameweek` object of the specified gameweek.

        :param int gameweek_id: A gameweek's id.
        """
        return Gameweek(gameweek_id)

    @staticmethod
    def game_settings():
        """
        Returns a dictionary containing the Fantasy Premier League's rules.
        """
        return requests.get(GAME_SETTINGS_URL).json()

    @staticmethod
    def get_classic_league(league_id):
        """
        Returns a `ClassicLeague` object with the given `league_id`.

        :param string league_id: A league's id
        """
        return ClassicLeague(league_id)

    @staticmethod
    def get_h2h_league(league_id):
        """
        Returns a `H2HLeague` object with the given `league_id`.

        :param string league_id: A league's id
        """
        return H2HLeague(league_id)
