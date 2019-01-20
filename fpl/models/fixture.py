from ..utils import team_converter
from .player import Player


def add_player(location, information):
    """Appends player to the location list."""
    player = Player(information["element"])
    goals = information["value"]
    location.append({"player": player, "goals": goals})


class Fixture():
    """A class representing fixtures in the Fantasy Premier League."""
    def __init__(self, fixture_information):
        for k, v in fixture_information.items():
            setattr(self, k, v)

    def _get_players(self, metric):
        """Helper function that returns a dictionary containing players for the
        given metric (away and home).
        """
        for statistic in self.stats:
            if metric in statistic.keys():
                player_information = statistic[metric]

        return player_information

    def get_goalscorers(self):
        """Returns all players who scored in the fixture."""
        if not self.finished:
            return

        return self._get_players("goals_scored")

    def get_assisters(self):
        """Returns all players who made an assist in the fixture."""
        if not self.finished:
            return

        return self._get_players("assists")

    def get_own_goalscorers(self):
        """Returns all players who scored an own goal in the fixture."""
        if not self.finished:
            return

        return self._get_players("own_goals")

    def get_yellow_cards(self):
        """Returns all players who received a yellow card in the fixture."""
        if not self.finished:
            return

        return self._get_players("yellow_cards")

    def get_red_cards(self):
        """Returns all players who received a red card in the fixture."""
        if not self.finished:
            return

        return self._get_players("red_cards")

    def get_penalty_saves(self):
        """Returns all players who saved a penalty in the fixture."""
        if not self.finished:
            return

        return self._get_players("penalties_saved")

    def get_penalty_misses(self):
        """Returns all players who missed a penalty in the fixture."""
        if not self.finished:
            return

        return self._get_players("penalties_missed")

    def get_saves(self):
        """Returns all players who made a save in the fixture."""
        if not self.finished:
            return

        return self._get_players("saves")

    def get_bonus(self):
        """Returns all players who received bonus points in the fixture."""
        if not self.finished:
            return

        return self._get_players("bonus")

    def get_bps(self):
        """Returns the bonus points of each player."""
        if not self.finished:
            return

        return self._get_players("bps")
