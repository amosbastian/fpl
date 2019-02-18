from ..utils import team_converter
from .player import Player


def add_player(location, information):
    """Appends player to the location list."""
    player = Player(information["element"])
    goals = information["value"]
    location.append({"player": player, "goals": goals})


class Fixture():
    """A class representing fixtures in the Fantasy Premier League.

    Basic usage::

      >>> from fpl import FPL
      >>> import aiohttp
      >>> import asyncio
      >>>
      >>> async def main():
      ...     async with aiohttp.ClientSession() as session:
      ...         fpl = FPL(session)
      ...         fixture = await fpl.get_fixture(1)
      ...     print(fixture)
      ...
      >>> asyncio.run(main())
      Arsenal vs. Man City - 10 Aug 19:00
    """
    def __init__(self, fixture_information):
        for k, v in fixture_information.items():
            setattr(self, k, v)

    def _get_players(self, metric):
        """Helper function that returns a dictionary containing players for the
        given metric (away and home).
        """
        stats = getattr(self, "stats", [])
        for statistic in stats:
            if metric in statistic.keys():
                return statistic[metric]

        return {}

    def get_goalscorers(self):
        """Returns all players who scored in the fixture.

        :rtype: dict
        """
        if not getattr(self, "finished", False):
            return {}

        return self._get_players("goals_scored")

    def get_assisters(self):
        """Returns all players who made an assist in the fixture.

        :rtype: dict
        """
        if not getattr(self, "finished", False):
            return {}

        return self._get_players("assists")

    def get_own_goalscorers(self):
        """Returns all players who scored an own goal in the fixture.

        :rtype: dict
        """
        if not getattr(self, "finished", False):
            return {}

        return self._get_players("own_goals")

    def get_yellow_cards(self):
        """Returns all players who received a yellow card in the fixture.

        :rtype: dict
        """
        if not getattr(self, "finished", False):
            return {}

        return self._get_players("yellow_cards")

    def get_red_cards(self):
        """Returns all players who received a red card in the fixture.

        :rtype: dict
        """
        if not getattr(self, "finished", False):
            return {}

        return self._get_players("red_cards")

    def get_penalty_saves(self):
        """Returns all players who saved a penalty in the fixture.

        :rtype: dict
        """
        if not getattr(self, "finished", False):
            return {}

        return self._get_players("penalties_saved")

    def get_penalty_misses(self):
        """Returns all players who missed a penalty in the fixture.

        :rtype: dict
        """
        if not getattr(self, "finished", False):
            return {}

        return self._get_players("penalties_missed")

    def get_saves(self):
        """Returns all players who made a save in the fixture.

        :rtype: dict
        """
        if not getattr(self, "finished", False):
            return {}

        return self._get_players("saves")

    def get_bonus(self):
        """Returns all players who received bonus points in the fixture.

        :rtype: dict
        """
        if not getattr(self, "finished", False):
            return {}

        return self._get_players("bonus")

    def get_bps(self):
        """Returns the bonus points of each player.

        :rtype: dict
        """
        if not getattr(self, "finished", False):
            return {}

        return self._get_players("bps")

    def __str__(self):
        return (f"{team_converter(self.team_h)} vs. "
                f"{team_converter(self.team_a)} - "
                f"{self.deadline_time_formatted}")
