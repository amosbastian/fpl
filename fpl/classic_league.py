import itertools
import requests

API_BASE_URL = "https://fantasy.premierleague.com/drf/"


class ClassicLeague(object):
    """
    A class representing a classic league in the Fantasy Premier League.
    """
    def __init__(self, league_id):
        self.id = league_id
        self._information = self._get_information()
        self._league = self._information["league"]

        #: A dictionary containing information about new entries to the league.
        self.new_entries = self._information["new_entries"]

        #: The name of the league.
        self.name = self._league["name"]
        #: The date the league was created.
        self.created = self._league["created"]
        #: The gameweek the league started in.
        self.started = self._league["start_event"]

        self.standings = self._standings()
        """
        A list (of dictionaries) containing information about the league's
        standings.
        """

    @property
    def type(self):
        """The type of league that the league is."""
        return self._league["league_type"]

    def _get_information(self):
        """Returns information about the given league."""
        return requests.get("{}leagues-classic-standings/{}".format(
            API_BASE_URL, self.id)).json()

    def _standings(self):
        """Returns league standings for all teams."""
        standings = []
        # Iterate through all available pages
        for page in itertools.count(start=1):
            url = "{}leagues-classic-standings/{}?ls-page={}".format(
                API_BASE_URL, self.id, page)
            page_results = requests.get(url).json()['standings']['results']
            # Check if page exists
            if page_results:
                standings.extend(page_results)
            else:
                return standings

    def __str__(self):
        return "{} - {}".format(self.name, self.id)
