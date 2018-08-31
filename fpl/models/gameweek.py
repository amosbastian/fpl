import requests

from ..constants import API_URLS
from .player import Player


class Gameweek():
    """A class representing a gameweek of the Fantasy Premier League."""
    def __init__(self, gameweek_id):
        self.gameweek_id = int(gameweek_id)

        self._additional = self._get_additional()
        self._specific = self._get_specific()

        #: A `datetime` object of the gameweek's deadline.
        self.deadline = self._specific["deadline_time"]
        #: A boolean that signifies if the gameweek is already finished.
        self.finished = self._specific["finished"]
        #: The name of the gameweek, e.g. "Gameweek 1".
        self.name = self._specific["name"]

        #: A boolean that signifies if the gameweek is the current gameweek.
        self.is_current = self._specific["is_current"]
        #: A boolean that signifies if the gameweek is the next gameweek.
        self.is_next = self._specific["is_next"]
        #: A boolean that signifies if the gameweek is the previous gameweek.
        self.is_previous = self._specific["is_previous"]

        #: The average score of the gameweek.
        self.average_score = self._specific["average_entry_score"]
        #: The `user_id` of the best player of the gameweek.
        self.best_player = self._specific["highest_scoring_entry"]
        #: The highest score of the gameweek.
        self.highest_score = self._specific["highest_score"]
        #: The players that played in the gameweek.
        self.players = None

    @property
    def fixtures(self):
        """A list of dictionaries containing information about the fixtures of
        the gameweek.
        """
        return self._additional["fixtures"]

    def get_players(self):
        """Returns a list of players that played in the gameweek."""
        player_ids = [int(player_id) for player_id
                      in self._additional["elements"].keys()]
        response = requests.get(API_URLS["players"]).json()
        players = [Player(player["id"], player) for player in response
                   if player["id"] in player_ids]

        self.players = players

    def _get_specific(self):
        response = requests.get(API_URLS["gameweeks"]).json()
        return response[self.gameweek_id - 1]

    def _get_additional(self):
        return requests.get(API_URLS["gameweek_live"].format(
            self.gameweek_id)).json()

    def __str__(self):
        return "{} - {}".format(self.name, self.deadline)
