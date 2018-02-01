import json
import requests

API_BASE_URL = "https://fantasy.premierleague.com/drf/"

class Gameweek(object):
    """
    A class representing a gameweek of the Fantasy Premier League.
    """
    def __init__(self, gameweek_id):
        self.id = gameweek_id
        
        self._additional = self._additional()
        self._specific = self._specific()

        # General gameweek information
        self.deadline = self._specific["deadline_time"]
        self.finished = self._specific["finished"]
        self.name = self._specific["name"]

        self.is_current = self._specific["is_current"]
        self.is_next = self._specific["is_next"]
        self.is_previous = self._specific["is_previous"]

        # Gameweek score information
        self.average_score = self._specific["average_entry_score"]
        self.best_player = self._specific["highest_scoring_entry"]
        self.highest_score = self._specific["highest_score"]

    @property
    def fixtures(self):
        return self._additional["fixtures"]

    @property
    def players(self):
        return self._additional["players"]

    def _specific(self):
        response = requests.get("{}events".format(API_BASE_URL)).json()
        return response[self.id - 1]

    def _additional(self):
        return requests.get("{}event/{}/live".format(API_BASE_URL,
            self.id)).json()

    def __str__(self):
        return "{} - {}".format(self.name, self.deadline)