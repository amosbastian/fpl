import asyncio

from ..constants import API_URLS
from ..utils import fetch, get_current_gameweek


class H2HLeague():
    """
    A class representing a h2h league in the Fantasy Premier League.
    """
    def __init__(self, league_information, session=None):
        self._session = session

        for k, v in league_information.items():
            setattr(self, k, v)

    def __str__(self):
        return f"{self.league['name']} - {self.league['id']}"

    async def get_fixtures(self, gameweek=None):
        """Returns h2h results/fixtures for given league, login required."""
        if not self._session:
            return

        if gameweek:
            gameweeks = range(gameweek, gameweek + 1)
        else:
            current_gameweek = await get_current_gameweek(self._session)
            gameweeks = range(1, current_gameweek + 1)

        tasks = [asyncio.ensure_future(
                 fetch(self._session,
                       API_URLS["h2h"].format(self.league["id"], page)))
                 for page in gameweeks]

        fixtures = await asyncio.gather(*tasks)

        return fixtures
