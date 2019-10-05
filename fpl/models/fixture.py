from ..utils import team_converter
from .player import Player
from datetime import datetime


def add_player(location, information):
    """Appends player to the location list."""
    player = Player(information["element"])
    goals = information["value"]
    location.append({"player": player, "goals": goals})


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
            if k == 'stats':
                v = {w['identifier']: {'a': w['a'], 'h': w['h']} for w in v}
            setattr(self, k, v)

    def _get_players(self, metric):  # no longer used
        """Helper function that returns a dictionary containing players for the
        given metric (away and home).
        """
        stats = getattr(self, "stats", [])
        for statistic in stats:
            if metric == statistic['identifier']:
                # # merge home and away player lists and sort in descending order
                # return sorted(statistic['a'] + statistic['h'], key=lambda x: x['value'], reverse=True)
                print(metric, statistic)
                return statistic
        return {}

    def get_goalscorers(self):
        """Returns all players who scored in the fixture.
        :rtype: dict
        """
        try:
            return self.stats["goals_scored"]
        except KeyError:
            return {'a': [], 'h': []}

    def get_assisters(self):
        """Returns all players who made an assist in the fixture.

        :rtype: dict
        """
        try:
            return self.stats["assists"]
        except KeyError:
            return {'a': [], 'h': []}

    def get_own_goalscorers(self):
        """Returns all players who scored an own goal in the fixture.
        :rtype: dict
        """
        try:
            return self.stats["own_goals"]
        except KeyError:
            return {'a': [], 'h': []}

    def get_yellow_cards(self):
        """Returns all players who received a yellow card in the fixture.

        :rtype: dict
        """
        try:
            return self.stats["yellow_cards"]
        except KeyError:
            return {'a': [], 'h': []}

    def get_red_cards(self):
        """Returns all players who received a red card in the fixture.

        :rtype: dict
        """
        try:
            return self.stats["red_cards"]
        except KeyError:
            return {'a': [], 'h': []}

    def get_penalty_saves(self):
        """Returns all players who saved a penalty in the fixture.

        :rtype: dict
        """
        try:
            return self.stats["penalties_saved"]
        except KeyError:
            return {'a': [], 'h': []}

    def get_penalty_misses(self):
        """Returns all players who missed a penalty in the fixture.

        :rtype: dict
        """
        try:
            return self.stats["penalties_missed"]
        except KeyError:
            return {'a': [], 'h': []}

    def get_saves(self):
        """Returns all players who made a save in the fixture.

        :rtype: dict
        """
        try:
            return self.stats["saves"]
        except KeyError:
            return {'a': [], 'h': []}

    def get_bonus(self, provisional=False):
        """Returns all players who received bonus points in the fixture.

        :rtype: dict
        """
        if self.finished:
            return self.stats["bonus"]
        elif self.started and provisional:
            bps = self.get_bps()
            home = [b["element"] for b in bps['h']]
            away = [b["element"] for b in bps['a']]
            bps = bps['a'] + bps['h']
            bps = {b["element"]: b["value"] for b in bps}  # map to dict
            bps_values = set(bps.values())

            try:
                bps1 = max(bps_values)  # highest bps
                bps_values.remove(bps1)
                bps2 = max(bps_values)  # 2nd highest bps
                bps_values.remove(bps2)
                bps3 = max(bps_values)  # 3rd highest bps
            except ValueError:  # empty set
                return {'a': [], 'h': []}

            else:
                bonus3 = list(filter(lambda x: bps[x] == bps1, bps.keys()))
                bonus2 = bonus1 = []
                if len(bonus3) == 1:
                    bonus2 = list(filter(lambda x: bps[x] == bps2, bps.keys()))
                if len(bonus3) + len(bonus2) == 2:
                    if len(bonus3) == 2:  # 2 way tie for 3 bonus
                        bonus1 = list(filter(lambda x: bps[x] == bps2, bps.keys()))
                    else:
                        bonus1 = list(filter(lambda x: bps[x] == bps3, bps.keys()))
                bonus3 = [{"value": 3, "element": b} for b in bonus3]
                bonus2 = [{"value": 2, "element": b} for b in bonus2]
                bonus1 = [{"value": 1, "element": b} for b in bonus1]
                bonus = bonus3 + bonus2 + bonus1
                h = []
                a = []
                for b in bonus:
                    if b["element"] in home:
                        h.append(b)
                    elif b["element"] in away:
                        a.append(b)
                return {'a': a, 'h': h}
        else:
            return {'a': [], 'h': []}

    def get_bps(self):
        """Returns the bonus points of each player.
        :rtype: dict
        """
        try:
            return self.stats["bps"]
        except KeyError:
            return {'a': [], 'h': []}

    def __str__(self):
        return (f"{team_converter(self.team_h)} vs. "
                f"{team_converter(self.team_a)} - "
                f"{self.kickoff_time}")
