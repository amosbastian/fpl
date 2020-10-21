from ..utils import date_formatter


class Gameweek():
    """A class representing a gameweek in Fantasy Premier League."""

    def __init__(self, gameweek_information):
        for k, v in gameweek_information.items():
            setattr(self, k, v)

    def __str__(self):
        return f"{self.name} - Deadline {date_formatter(self.deadline_time)}"
