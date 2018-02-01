import json
import requests

API_BASE_URL = "https://fantasy.premierleague.com/drf/"

class H2HLeague(object):
    """
    A class representing a h2h league in the Fantasy Premier League.
    """
    def __init__(self, league_id):
        self.id = league_id
        self._information = self._information()
        self._league = self._information["league"]

        #: A dictionary containing information about new entries to the league.
        self.new_entries = self._information["new_entries"]

        #: The name of the league.
        self.name = self._league["name"]
        #: The date the league was created.
        self.created = self._league["created"]
        #: The gameweek the league started in.
        self.started = self._league["start_event"]
        #: Information about the knockout rounds.
        self.ko_rounds = self._league["ko_rounds"]

        self.standings = self._information["standings"]["results"]
        """
        A list (of dictionaries) containing information about the league's
        standings.
        """

    @property
    def type(self):
        """The type of league that the league is."""
        return self._league["league_type"]

    def _information(self):
        """Returns information about the given league."""
        return requests.get("{}leagues-h2h-standings/{}".format(
            API_BASE_URL, self.id)).json()

    def __str__(self):
        return "{} - {}".format(self.name, self.id)