from ..constants import API_URLS
from ..utils import fetch, position_converter, team_converter


class Player():
    """A class representing a player in Fantasy Premier League."""

    def __init__(self, player_information, session):
        self._session = session
        for k, v in player_information.items():
            setattr(self, k, v)

    @property
    async def games_played(self):
        """The number of games where the player has played at least 1 minute.

        :rtype: int
        """
        if hasattr(self, "history"):
            fixtures = self.history
        else:
            player_summary = await fetch(
                self._session, API_URLS["player"].format(self.id))
            fixtures = player_summary["history"]

        return sum([1 for fixture in fixtures if fixture["minutes"] > 0])

    @property
    def pp90(self):
        """Points per 90 minutes.

        :rtype: float
        """
        minutes = float(getattr(self, "minutes", 0))

        if minutes == 0:
            return 0.0

        return getattr(self, "total_points", 0.0) / minutes * 90.0

    @property
    async def vapm(self):
        """Value added per million.

        :rtype: float
        """
        games_played = await self.games_played
        cost = getattr(self, "now_cost", 0)

        if games_played == 0 or cost == 0:
            return 0.0

        return (getattr(self, "total_points", 0.0) / games_played - 2) / (cost / 10)

    def __str__(self):
        return (f"{self.web_name} - "
                f"{position_converter(self.element_type)} - "
                f"{team_converter(self.team)}")


class PlayerSummary:
    """A class representing a player in the Fantasy Premier League's summary.
    """

    def __init__(self, player_summary):
        for k, v in player_summary.items():
            setattr(self, k, v)
