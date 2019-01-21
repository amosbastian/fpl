from ..constants import API_URLS
from ..utils import team_converter, position_converter


class Player():
    """A class representing a player in the Fantasy Premier League."""
    def __init__(self, player_information):
        for k, v in player_information.items():
            setattr(self, k, v)

    @property
    def games_played(self):
        """Returns the amount of games a player has played in."""
        return sum([1 for fixture in self.fixtures if fixture["minutes"] > 0])

    @property
    def pp90(self):
        """Returns the amount of points a player scores per 90 minutes played.
        """
        if self.minutes == 0:
            return 0
        return self.total_points / float(self.minutes)

    def __str__(self):
        return "{} - {} - {}".format(self.name, self.position, self.team)


class PlayerSummary:
    """A class representing a player in the Fantasy Premier League's summary.
    """
    def __init__(self, player_summary):
        for k, v in player_summary.items():
            setattr(self, k, v)
