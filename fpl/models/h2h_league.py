import itertools
import requests

from ..constants import API_URLS


class H2HLeague():
    """
    A class representing a h2h league in the Fantasy Premier League.
    """
    def __init__(self, league_id, session=None):
        self.league_id = league_id
        self._information = self._get_information()
        self._league = self._information["league"]
        #: Session for H2H fixtures
        self._session = session

        #: A dictionary containing information about new entries to the league.
        self.new_entries = self._information["new_entries"]

        #: The name of the league.
        self.name = self._league["name"]
        #: Whether the league has started or not.
        self.has_started = self._league["has_started"]
        #: Whether or not the league can be deleted.
        self.can_delete = self._league["can_delete"]
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
        #: Information about the knockout rounds.
        self.ko_rounds = self._league["ko_rounds"]
        #: Admin entry.
        self.admin_entry = self._league["admin_entry"]
        #: The gameweek the league started in.
        self.started = self._league["start_event"]
        #: The fixtures of the league.
        self.fixtures = None

    def _get_information(self):
        """Returns information about the given league."""
        return requests.get(API_URLS["league_h2h"].format(
            self.league_id)).json()

    def __str__(self):
        return "{} - {}".format(self.name, self.league_id)

    def get_fixtures(self):
        """Returns h2h results/fixtures for given league, login required."""
        if not self._session:
            return

        fixtures = []
        for page in itertools.count(start=1):
            url = API_URLS["h2h"].format(self.league_id, page)
            page_results = self._session.get(url).json()["matches"]["results"]

            if page_results:
                fixtures.extend(page_results)
            else:
                self.fixtures = fixtures
                break
