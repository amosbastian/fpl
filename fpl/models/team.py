from ..constants import API_URLS
from ..utils import fetch
from .player import Player


class Team():
    """A class representing a real team in the Fantasy Premier League.

    Basic usage::

      >>> from fpl import FPL
      >>> import aiohttp
      >>> import asyncio
      >>>
      >>> async def main():
      ...     async with aiohttp.ClientSession() as session:
      ...         fpl = FPL(session)
      ...         team = await fpl.get_team(14)
      ...     print(team)
      ...
      >>> asyncio.run(main())
      Man Utd
    """
    def __init__(self, team_information, session):
        self._session = session
        for k, v in team_information.items():
            setattr(self, k, v)

    async def get_players(self, return_json=False):
        """Returns a list containing the players who play for the team. Does
        not include the player's summary.

        :param return_json: (optional) Boolean. If ``True`` returns a list of
            dicts, if ``False`` returns a list of Player objects. Defaults to
            ``False``.
        :type return_json: bool
        :rtype: list
        """
        team_players = getattr(self, "players", [])

        if not team_players:
            players = await fetch(self._session, API_URLS["static"])
            players = players["elements"]
            team_players = [player for player in players
                            if player["team"] == self.id]
            self.players = team_players

        if return_json:
            return team_players

        return [Player(player, self._session) for player in team_players]

    async def get_fixtures(self, return_json=False):
        """Returns a list containing the team's fixtures.

        :param return_json: (optional) Boolean. If ``True`` returns a list of
            dicts, if ``False`` returns a list of TeamFixture objects.
            Defaults to ``False``.
        :type return_json: bool
        :rtype: list
        """
        fixtures = getattr(self, "fixtures", [])
        if fixtures:
            return fixtures

        players = getattr(self, "players", [])
        if not players:
            await self.get_players()

        player = self.players[0]
        url = API_URLS["player"].format(player["id"])
        player_summary = await fetch(self._session, url)

        self.fixtures = player_summary["fixtures"]

        if return_json:
            return self.fixtures

        # TODO: create TeamFixture
        return self.fixtures

    def __str__(self):
        return self.name
