import json
import requests

API_BASE_URL = "https://fantasy.premierleague.com/drf/"

def team_converter(team_id):
    """
    Converts a team's ID to their actual name.
    """
    if team_id == 1:
        return "Arsenal"
    elif team_id == 2:
        return "Bournemouth"
    elif team_id == 3:
        return "Brighton"
    elif team_id == 4:
        return "Burnley"
    elif team_id == 5:
        return "Chelsea"
    elif team_id == 6:
        return "Crystal Palace"
    elif team_id == 7:
        return "Everton"
    elif team_id == 8:
        return "Huddersfield"
    elif team_id == 9:
        return "Leicester"
    elif team_id == 10:
        return "Liverpool"
    elif team_id == 11:
        return "Man City"
    elif team_id == 12:
        return "Man Utd"
    elif team_id == 13:
        return "Newcastle"
    elif team_id == 14:
        return "Southampton"
    elif team_id == 15:
        return "Stoke"
    elif team_id == 16:
        return "Swansea"
    elif team_id == 17:
        return "Spurs"
    elif team_id == 18:
        return "Watford"
    else:
        return "West Brom"

def position_converter(position):
    """
    Converts a player's `element_type` too their actual position.
    """
    if position == 1:
        return "Goalkeeper"
    elif position == 2:
        return "Defender"
    elif position == 3:
        return "Midfielder"
    else:
        return "Forward"

class Player(object):
    """
    A class representing a player in the Fantasy Premier League.
    """
    def __init__(self, player_id):
        self.id = player_id
        self._specific = self._specific()
        self._additional = self._additional()

        #: The player's web name.
        self.name = self._additional["web_name"]
        #: The player's first name.
        self.first_name = self._additional["first_name"]
        #: The player's second name.
        self.second_name = self._additional["second_name"]

        #: The player's points in the current gameweek.
        self.gameweek_points = self._additional["event_points"]
        #: The player's price change in the current gameweek.
        self.gameweek_price_change = self._additional["cost_change_event"]
        #: The player's transfers in in the current gameweek.
        self.gameweek_transfers_in = self._additional["transfers_in_event"]
        #: The player's transfers out in the current gameweek.
        self.gameweek_transfers_out = self._additional["transfers_out_event"]
        #: The player's transfers in in the current season.
        self.transfers_in = self._additional["transfers_in"]
        #: The player's transfers out in the current season.
        self.transfers_out = self._additional["transfers_out"]

        #: The player's current price.
        self.price = self._additional["now_cost"] / 10.0
        #: The amount of goals scored by the player.
        self.goals = self._additional["goals_scored"]
        #: The amount of goals assisted by the player.
        self.assists = self._additional["assists"]
        #: The amount of clean sheets the player has had.
        self.clean_sheets = self._additional["clean_sheets"]
        #: The amount of saves the player has made.
        self.saves = self._additional["saves"]
        #: The amount of points the player scores per game on average.
        self.ppg = self._additional["points_per_game"]
        #: The amount of minutes the player has played.
        self.minutes = self._additional["minutes"]
        #: The amount of bonus points the player has scored.
        self.bps = self._additional["bps"]
        #: The amount of penalties the player has missed.
        self.penalties_missed = self._additional["penalties_missed"]
        #: The amount of yellow cards the player has received.
        self.yellow_cards = self._additional["yellow_cards"]
        #: The amount of red cards the player has received.
        self.red_cards = self._additional["red_cards"]
        #: The percentage of users the player is selected by.
        self.selected_by = float(self._additional["selected_by_percent"])
        #: The ID of the team the player plays for.
        self.team_id = self._additional["team"]
        #: The type of player the player is (1, 2, 3 or 4).
        self.type = self._additional["element_type"]


    @property
    def status(self):
        """The status of the player, which can be available, injured or ..."""
        return self._additional["status"]

    @property
    def team(self):
        """A `Team` object of the team the player plays for."""
        return team_converter(self.team_id)

    @property
    def position(self):
        """The position that the player plays in."""
        return position_converter(self.type)

    @property
    def explain(self):
        """Information about the player's upcoming fixture."""
        return self._specific["explain"]

    @property
    def fixtures(self):
        """List of the player's upcoming fixtures."""
        return self._specific["fixtures"]

    @property
    def history_summary(self):
        """List of the player's performance in his three most recent games."""
        return self._specific["history_summary"]

    @property
    def fixtures_summary(self):
        """List of the player's closest three upcoming fixtures."""
        return self._specific["fixtures_summary"]

    @property
    def history_past(self):
        """List of a summary of the player's performance in previous seasons."""
        return self._specific["history_past"]

    @property
    def history(self):
        """List of the player's performance in fixtures of this season."""
        return self._specific["history"]

    def _specific(self):
        """
        Returns the player with the specific player_id.
        """
        return requests.get("{}element-summary/{}".format(API_BASE_URL,
            self.id)).json()

    def _additional(self):
        """
        Returns additional information that isn't included in the other list of
        players.
        """
        response = requests.get("{}elements".format(API_BASE_URL)).json()
        for player in response:
            if player["id"] == self.id:
                return player

    def __str__(self):
        return "{} - {} - {}".format(player.name, player.position, player.team)