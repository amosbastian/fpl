from ..constants import API_URLS
from ..utils import fetch


class ClassicLeague():
    """A class representing a classic league in the Fantasy Premier League."""
    def __init__(self, league_information, session):
        self._session = session

        for k, v in league_information.items():
            setattr(self, k, v)

    async def get_standings(self, page):
        """Returns the league's standings of the given page."""
        url = "{}?ls-page={}".format(
                API_URLS["league_classic"].format(self.league["id"]), page)
        standings = await fetch(self._session, url)
        return standings["standings"]

    def __str__(self):
        return f"{self.league['name']} - {self.league['id']}"
