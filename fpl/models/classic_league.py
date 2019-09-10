from ..constants import API_URLS
from ..utils import fetch


class ClassicLeague():
    """A class representing a classic league in the Fantasy Premier League.

    Basic usage::

      >>> from fpl import FPL
      >>> import aiohttp
      >>> import asyncio
      >>>
      >>> async def main():
      ...     async with aiohttp.ClientSession() as session:
      ...         fpl = FPL(session)
      ...         await fpl.login()
      ...         classic_league = await fpl.get_classic_league(1137)
      ...     print(classic_league)
      ...
      >>> asyncio.run(main())
      Official /r/FantasyPL Classic League - 1137
    """
    def __init__(self, league_information, session):
        self._session = session

        for k, v in league_information.items():
            setattr(self, k, v)

    async def get_standings(self, page=1, page_new_entries=1, phase=1):
        """Returns the league's standings of the given page.

        Information is taken from e.g.:
            https://fantasy.premierleague.com/api/leagues-classic/967/standings/?page_new_entries=1&page_standings=1&phase=1

        :param page: A page of the league's standings (default is 50 managers
            per page).
        :type page: string or int
        :rtype: dict
        """
        if hasattr(self, "standings") and self.standings["page"] == page:
            return self.standings

        url = "{}?page_new_entries={}&page_standings={}&phase={}".format(
                API_URLS["league_classic"].format(self.league["id"]),
                page_new_entries, page, phase)
        standings = await fetch(self._session, url)
        self.standings = standings["standings"]

        return standings["standings"]

    def __str__(self):
        return f"{self.league['name']} - {self.league['id']}"
