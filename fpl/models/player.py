import requests

from ..constants import API_URLS
from ..utils import team_converter, position_converter


class Player():
    """A class representing a player in the Fantasy Premier League."""
    def __init__(self, player):
        self.id = player["id"]

        #: The amount of goals assisted by the player.
        self.assists = player["assists"]
        #: The amount of bonus points the player has scored.
        self.bps = player["bps"]
        #: The amount of clean sheets the player has had.
        self.clean_sheets = player["clean_sheets"]
        #: The player's first name.
        self.first_name = player["first_name"]
        #: The player's form.
        self.form = player["form"]
        #: The player's points in the current gameweek.
        self.gameweek_points = player["event_points"]
        #: The player's price change in the current gameweek.
        self.gameweek_price_change = player["cost_change_event"]
        #: The player's transfers in in the current gameweek.
        self.gameweek_transfers_in = player["transfers_in_event"]
        #: The player's transfers out in the current gameweek.
        self.gameweek_transfers_out = player["transfers_out_event"]
        #: The amount of goals scored by the player.
        self.goals = player["goals_scored"]
        #: The amount of minutes the player has played.
        self.minutes = player["minutes"]
        #: The player's web name.
        self.name = player["web_name"]
        #: News about the player.
        self.news = player["news"]
        #: The amount of penalties the player has missed.
        self.penalties_missed = player["penalties_missed"]
        #: The type of player the player is (1, 2, 3 or 4).
        self.player_type = player["element_type"]
        #: The amount of points a player has scored this season.
        self.points = player["total_points"]
        #: The position that the player plays in.
        self.position = position_converter(self.player_type)
        #: The amount of points the player scores per game on average.
        self.ppg = player["points_per_game"]
        #: The player's current price.
        self.price = player["now_cost"] / 10.0
        #: The amount of red cards the player has received.
        self.red_cards = player["red_cards"]
        #: The amount of saves the player has made.
        self.saves = player["saves"]
        #: The player's second name.
        self.second_name = player["second_name"]
        #: The percentage of users the player is selected by.
        self.selected_by = float(player["selected_by_percent"])
        #: The status of the player, which can be available, injured or ...
        self.status = player["status"]
        #: The player's squad number.
        self.squad_number = player["squad_number"]
        #: The ID of the team the player plays for.
        self.team_id = player["team"]
        #: The team the player currently plays for.
        self.team = team_converter(self.team_id)
        #: The player's transfers in in the current season.
        self.transfers_in = player["transfers_in"]
        #: The player's transfers out in the current season.
        self.transfers_out = player["transfers_out"]
        #: The amount of yellow cards the player has received.
        self.yellow_cards = player["yellow_cards"]
        #: The player's expected points in this gameweek.
        self.ep_this = player["ep_this"]
        #: The player's expected points in the next gameweek.
        self.ep_next = player["ep_next"]

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
        return self.points / float(self.minutes)

    def __str__(self):
        return "{} - {} - {}".format(self.name, self.position, self.team)


class PlayerSummary:
    """A class representing a player in the Fantasy Premier League's summary.
    """
    def __init__(self, player_summary):
        #: Information about the player's upcoming fixture.
        self.explain = player_summary["explain"]
        #: List of the player's upcoming fixtures.
        self.fixtures = player_summary["fixtures"]
        #: List of the player's closest three upcoming fixtures.
        self.fixtures_summary = player_summary["fixtures_summary"]
        #: List of the player's performance in fixtures of the current season.
        self.history = player_summary["history"]
        #: List of a summary of the player's performance in previous seasons.
        self.history_past = player_summary["history_past"]
        #: List of the player's performance in his three most recent games.
        self.history_summary = player_summary["history_summary"]
