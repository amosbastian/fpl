from ..constants import API_URLS
from ..utils import fetch
from .fixture import Fixture
from .player import Player


class Team():
    """A class representing a real team in the Fantasy Premier League."""
    def __init__(self, team_information, session):
        self.session = session
        for k, v in team_information.items():
            setattr(self, k, v)

    async def get_players(self, return_json=False):
        """Sets the `players` property as a list of players that play for the
        team.

        :param boolean return_json: Flag for returning JSON
        """
        if hasattr(self, "players"):
            players = self.players
        else:
            players = await fetch(self.session, API_URLS["players"])

        team_players = [player for player in players
                        if player["team"] == self.id]
        self.players = team_players

        if return_json:
            return team_players
        return [Player(player) for player in team_players]

    async def get_fixtures(self, return_json=False):
        """Sets the team's fixtures equal to that of one of its player's
        fixtures.

        :param boolean return_json: Flag for returning JSON
        """
        if hasattr(self, "fixtures"):
            return self.fixtures

        if not hasattr(self, "players"):
            await self.get_players()

        print(self.players)

        player = self.players[0]
        url = API_URLS["player"].format(player["id"])
        player_summary = await fetch(self.session, url)

        self.fixtures = player_summary["fixtures"]

        if return_json:
            return self.fixtures

        # TODO: create TeamFixture
        return self.fixtures

    def __str__(self):
        return self.name
