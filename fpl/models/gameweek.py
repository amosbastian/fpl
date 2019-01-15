import requests

from ..constants import API_URLS
from .player import Player


class Gameweek():
    """A class representing a gameweek of the Fantasy Premier League."""
    def __init__(self, gameweek_information):
        self.id = gameweek_information["id"]
        #: A `datetime` object of the gameweek's deadline.
        self.deadline = gameweek_information["deadline_time"]
        #: A boolean that signifies if the gameweek is already finished.
        self.finished = gameweek_information["finished"]
        #: The name of the gameweek, e.g. "Gameweek 1".
        self.name = gameweek_information["name"]

        #: A boolean that signifies if the gameweek is the current gameweek.
        self.is_current = gameweek_information["is_current"]
        #: A boolean that signifies if the gameweek is the next gameweek.
        self.is_next = gameweek_information["is_next"]
        #: A boolean that signifies if the gameweek is the previous gameweek.
        self.is_previous = gameweek_information["is_previous"]

        #: The average score of the gameweek.
        self.average_score = gameweek_information["average_entry_score"]
        #: The `user_id` of the best player of the gameweek.
        self.best_player = gameweek_information["highest_scoring_entry"]
        #: The highest score of the gameweek.
        self.highest_score = gameweek_information["highest_score"]

        #: The fixtures of the gameweek.
        self.fixtures = gameweek_information["fixtures"]
        #: The players that played in the gameweek.
        self.players = gameweek_information["elements"]

    def __str__(self):
        return "{} - {}".format(self.name, self.deadline)
