import itertools
import requests

from ..constants import API_URLS


class ClassicLeague():
    """A class representing a classic league in the Fantasy Premier League."""
    def __init__(self, league_id):
        self.league_id = league_id
        self._information = self._get_information()
        self._league = self._information["league"]

        #: A dictionary containing information about new entries to the league.
        self.new_entries = self._information["new_entries"]

        #: The name of the league.
        self.name = self._league["name"]
        #: The shortname of the league.
        self.short_name = self._league["short_name"]
        #: The date the league was created.
        self.created = self._league["created"]
        #: Whether the league is closed or not.
        self.closed = self._league["closed"]
        #: Whether the league's forum is disabled.
        self.forum_disabled = self._league["forum_disabled"]
        #: Whether the league is public.
        self.is_public = self._league["make_code_public"]
        #: The league's rank.
        self.rank = self._league["rank"]
        #: The league's size.
        self.size = self._league["size"]
        #: The league's type.
        self.league_type = self._league["league_type"]
        #: The scoring system the league uses.
        self.scoring_system = self._league["_scoring"]
        #: Whether the standings are being reprocessed.
        self.reprocessing_standings = self._league["reprocess_standings"]
        #: Admin entry.
        self.admin_entry = self._league["admin_entry"]
        #: The gameweek the league started in.
        self.started = self._league["start_event"]
        #: The standings of the league.
        self.standings = None

    def _get_information(self):
        """Returns information about the given league."""
        return requests.get(API_URLS["league_classic"].format(self.league_id)).json()

    def get_standings(self):
        """Returns league standings for all teams in the league."""
        standings = []

        for page in itertools.count(start=1):
            url = "{}?ls-page={}".format(
                API_URLS["league_classic"].format(self.league_id), page)
            page_results = requests.get(url).json()["standings"]["results"]

            if page_results:
                standings.extend(page_results)
            else:
                self.standings = standings
                break

    def __str__(self):
        return "{} - {}".format(self.name, self.league_id)
