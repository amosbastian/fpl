import itertools
import requests

from ..constants import API_URLS


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

    @property
    def type(self):
        """The type of league that the league is."""
        return self._league["league_type"]

    def _get_information(self):
        """Returns information about the given league."""
        return requests.get(API_URLS["league_classic"].format(self.id)).json()

    def _standings(self):
        """Returns league standings for all teams."""
        standings = []

        for page in itertools.count(start=1):
            url = "{}?ls-page={}".format(
                API_URLS["league_classic"].format(self.id), page)
            page_results = requests.get(url).json()['standings']['results']

            if page_results:
                standings.extend(page_results)
            else:
                return standings

    def __str__(self):
        return "{} - {}".format(self.name, self.id)
