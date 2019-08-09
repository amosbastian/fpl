from ..utils import team_converter, position_converter


class Player():
    """A class representing a player in the Fantasy Premier League.

    Basic usage::

      >>> from fpl import FPL
      >>> import aiohttp
      >>> import asyncio
      >>>
      >>> async def main():
      ...     async with aiohttp.ClientSession() as session:
      ...         fpl = FPL(session)
      ...         player = await fpl.get_player(302)
      ...     print(player)
      ...
      >>> asyncio.run(main())
      Pogba - Midfielder - Man Utd
    """

    def __init__(self, player_information):
        for k, v in player_information.items():
            setattr(self, k, v)

    @property
    def games_played(self):
        """The number of games where the player has played at least 1 minute.

        :rtype: int
        """
        return sum([1 for fixture in getattr(self, "fixtures", [])
                    if fixture["minutes"] > 0])

    @property
    def pp90(self):
        """Points per 90 minutes.

        :rtype: float
        """
        minutes = getattr(self, "minutes", 0)
        if minutes == 0:
            return 0.0
        return getattr(self, "total_points", 0.0) / 90.0

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
