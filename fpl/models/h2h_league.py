import itertools
import requests

from ..constants import API_URLS


class H2HLeague(object):
    """
    A class representing a h2h league in the Fantasy Premier League.
    """
    def __init__(self, league_id, session=None):
        self.id = league_id
        self._information = self._get_information()
        self._league = self._information["league"]
        #: Session for H2H fixtures
        self._session = session

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

        self.fixtures = self._fixtures()
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
        return requests.get(API_URLS["league_h2h"].format(self.id)).json()

    def __str__(self):
        return "{} - {}".format(self.name, self.id)

    def _fixtures(self):
        """Returns h2h results/fixtures for given league, login required."""
        if not self._session:
            return []

        fixtures = []
        for page in itertools.count(start=1):
            url = API_URLS["h2h"].format(self.id, page)
            page_results = self._session.get(url).json()["matches"]["results"]

            if page_results:
                fixtures.extend(page_results)
            else:
                return fixtures
