import requests

API_BASE_URL = "https://fantasy.premierleague.com/drf/"


class Gameweek(object):
    """
    A class representing a gameweek of the Fantasy Premier League.
    """
    def __init__(self, gameweek_id):
        self.id = gameweek_id

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

    @property
    def fixtures(self):
        """
        A list of dictionaries containing information about the fixtures of
        the gameweek.
        """
        return self._additional["fixtures"]

    @property
    def players(self):
        """
        Returns a dictionary containing all players that played in the gameweek
        """
        return self._additional["elements"]

    def _get_specific(self):
        response = requests.get("{}events".format(API_BASE_URL)).json()
        return response[self.id - 1]

    def _get_additional(self):
        return requests.get(
            "{}event/{}/live".format(API_BASE_URL, self.id)).json()

    def __str__(self):
        return "{} - {}".format(self.name, self.deadline)
