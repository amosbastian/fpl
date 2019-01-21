from ..constants import API_URLS


class Gameweek():
    """A class representing a gameweek of the Fantasy Premier League."""
    def __init__(self, gameweek_information):
        for k, v in gameweek_information.items():
            setattr(self, k, v)

    def __str__(self):
        return "{} - {}".format(self.name, self.deadline_time_formatted)
