from ..utils import team_converter
from .player import Player


def add_player(location, information):
    """Appends player to the location list."""
    player = Player(information["element"])
    goals = information["value"]
    location.append({"player": player, "goals": goals})


# noinspection PyUnresolvedReferences
class Fixture:
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
            if k == "stats":
                v = {w["identifier"]: {"a": w["a"], "h": w["h"]} for w in v}
            setattr(self, k, v)

    def get_goalscorers(self):
        """Returns all players who scored in the fixture.

        :rtype: dict
        """
        try:
            return self.stats["goals_scored"]
        except KeyError:
            return {"a": [], "h": []}

    def get_assisters(self):
        """Returns all players who made an assist in the fixture.

        :rtype: dict
        """
        try:
            return self.stats["assists"]
        except KeyError:
            return {"a": [], "h": []}

    def get_own_goalscorers(self):
        """Returns all players who scored an own goal in the fixture.

        :rtype: dict
        """
        try:
            return self.stats["own_goals"]
        except KeyError:
            return {"a": [], "h": []}

    def get_yellow_cards(self):
        """Returns all players who received a yellow card in the fixture.

        :rtype: dict
        """
        try:
            return self.stats["yellow_cards"]
        except KeyError:
            return {"a": [], "h": []}

    def get_red_cards(self):
        """Returns all players who received a red card in the fixture.

        :rtype: dict
        """
        try:
            return self.stats["red_cards"]
        except KeyError:
            return {"a": [], "h": []}

    def get_penalty_saves(self):
        """Returns all players who saved a penalty in the fixture.

        :rtype: dict
        """
        try:
            return self.stats["penalties_saved"]
        except KeyError:
            return {"a": [], "h": []}

    def get_penalty_misses(self):
        """Returns all players who missed a penalty in the fixture.

        :rtype: dict
        """
        try:
            return self.stats["penalties_missed"]
        except KeyError:
            return {"a": [], "h": []}

    def get_saves(self):
        """Returns all players who made a save in the fixture.

        :rtype: dict
        """
        try:
            return self.stats["saves"]
        except KeyError:
            return {"a": [], "h": []}

    def get_bonus(self, provisional=False):
        """Returns all players who received bonus points in the fixture.

        :rtype: dict
        """
        if self.finished:
            return self.stats["bonus"]
        elif self.started and provisional:
            bps = self.get_bps()
            home = [b["element"] for b in bps["h"]]
            away = [b["element"] for b in bps["a"]]
            bps = bps["a"] + bps["h"]
            bps = {b["element"]: b["value"] for b in bps}
            bps_values = set(bps.values())

            try:
                bps_1st = max(bps_values)
                bps_values.remove(bps_1st)
                bps_2nd = max(bps_values)
                bps_values.remove(bps_2nd)
                bps_3rd = max(bps_values)
            except ValueError:
                return {"a": [], "h": []}

            else:
                bonus_3rd = list(
                    filter(lambda x: bps[x] == bps_1st, bps.keys()))
                bonus_2nd = bonus_1st = []

                if len(bonus_3rd) == 1:
                    bonus_2nd = list(
                        filter(lambda x: bps[x] == bps_2nd, bps.keys()))
                if len(bonus_3rd) + len(bonus_2nd) == 2:
                    # 2 way tie for 3 bonus
                    if len(bonus_3rd) == 2:
                        bonus_1st = list(
                            filter(lambda x: bps[x] == bps_2nd, bps.keys()))
                    else:
                        bonus_1st = list(
                            filter(lambda x: bps[x] == bps_3rd, bps.keys()))

                bonus_3rd = [{"value": 3, "element": b} for b in bonus_3rd]
                bonus_2nd = [{"value": 2, "element": b} for b in bonus_2nd]
                bonus_1st = [{"value": 1, "element": b} for b in bonus_1st]
                bonus = bonus_3rd + bonus_2nd + bonus_1st

                h = []
                a = []

                for b in bonus:
                    if b["element"] in home:
                        h.append(b)
                    elif b["element"] in away:
                        a.append(b)

                return {"a": a, "h": h}
        else:
            return {"a": [], "h": []}

    def get_bps(self):
        """Returns the bonus points of each player.

        :rtype: dict
        """
        try:
            return self.stats["bps"]
        except KeyError:
            return {"a": [], "h": []}

    def __str__(self):
        return (f"{team_converter(self.team_h)} vs. "
                f"{team_converter(self.team_a)} - "
                f"{self.kickoff_time}")
