import asyncio

from ..constants import API_URLS
from ..utils import fetch, logged_in


class H2HLeague:
    """
    A class representing a H2H league in the Fantasy Premier League.

    Basic usage::

      >>> from fpl import FPL
      >>> import aiohttp
      >>> import asyncio
      >>>
      >>> async def main():
      ...     async with aiohttp.ClientSession() as session:
      ...         fpl = FPL(session)
      ...         await fpl.login()
      ...         h2h_league = await fpl.get_h2h_league(760869)
      ...     print(h2h_league)
      ...
      >>> asyncio.run(main())
      League 760869 - 760869
    """

    def __init__(self, league_information, session):
        self._session = session
        for k, v in league_information.items():
            setattr(self, k, v)

    async def get_fixtures(self, gameweek=None):
        """Returns a list of fixtures / results of the H2H league.

        Information is taken from e.g.:
            https://fantasy.premierleague.com/api/leagues-h2h-matches/league/946125/?page=1

        :param gameweek: (optional) The gameweek of the fixtures / results.
        :type gameweek: string or int
        :rtype: list
        """
        if not self._session:
            return
        if not logged_in(self._session):
            raise Exception("Not authorized to get h2h fixtures. Log in.")
        else:
            url_query = ""
            if gameweek:
                url_query = f"event={gameweek}&"
            page = 1
            has_next = True
            results = []
            while has_next:
                fixtures = await asyncio.ensure_future(
                    fetch(self._session, API_URLS["league_h2h_fixtures"].format(self.league["id"], url_query, page)))
                has_next = fixtures['has_next']
                page = fixtures['page'] + 1
                results.extend(fixtures['results'])
            return results

    async def get_full_standings(self):
        standings = self.standings
        results = standings["results"]
        has_next = standings["has_next"]
        page = 1

        while has_next:
            page += 1
            standings_next = await asyncio.ensure_future(
                fetch(self._session, API_URLS["league_h2h"].format(self.league["id"], page)))
            results.extend(standings_next["results"])
            has_next = standings["has_next"]

        self.standings["results"] = results
        return results

    async def get_all_entries(self):
        await self.get_full_standings()
        return list(map(lambda x: x["entry"], self.standings["results"]))

    def __str__(self):
        return f"{self.league['name']} - {self.league['id']}"
