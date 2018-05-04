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
    return "West Brom"


def position_converter(position):
    """
    Converts a player's `element_type` to their actual position.
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
    def __init__(self, player_id, additional):
        self._id = player_id
        self._specific = self._get_specific()
        self._additional = additional

        #: The amount of goals assisted by the player.
        self.assists = self._additional["assists"]
        #: The amount of bonus points the player has scored.
        self.bps = self._additional["bps"]
        #: The amount of clean sheets the player has had.
        self.clean_sheets = self._additional["clean_sheets"]
        #: Information about the player's upcoming fixture.
        self.explain = self._specific["explain"]
        #: The player's first name.
        self.first_name = self._additional["first_name"]
        #: List of the player's upcoming fixtures.
        self.fixtures = self._specific["fixtures"]
        #: List of the player's closest three upcoming fixtures.
        self.fixtures_summary = self._specific["fixtures_summary"]
        #: The player's form.
        self.form = self._additional["form"]
        #: The amount of games a player has played in.
        self.games_played = self._games_played()
        #: The player's points in the current gameweek.
        self.gameweek_points = self._additional["event_points"]
        #: The player's price change in the current gameweek.
        self.gameweek_price_change = self._additional["cost_change_event"]
        #: The player's transfers in in the current gameweek.
        self.gameweek_transfers_in = self._additional["transfers_in_event"]
        #: The player's transfers out in the current gameweek.
        self.gameweek_transfers_out = self._additional["transfers_out_event"]
        #: The amount of goals scored by the player.
        self.goals = self._additional["goals_scored"]
        #: List of the player's performance in fixtures of the current season.
        self.history = self._specific["history"]
        #: List of a summary of the player's performance in previous seasons.
        self.history_past = self._specific["history_past"]
        #: List of the player's performance in his three most recent games.
        self.history_summary = self._specific["history_summary"]
        #: The amount of minutes the player has played.
        self.minutes = self._additional["minutes"]
        #: The player's web name.
        self.name = self._additional["web_name"]
        #: News about the player.
        self.news = self._additional["news"]
        #: The amount of penalties the player has missed.
        self.penalties_missed = self._additional["penalties_missed"]
        #: The type of player the player is (1, 2, 3 or 4).
        self.player_type = self._additional["element_type"]
        #: The amount of points a player has scored this season.
        self.points = self._additional["total_points"]
        #: The position that the player plays in.
        self.position = position_converter(self.player_type)
        #: The amount of points the player scores per game on average.
        self.ppg = self._additional["points_per_game"]
        #: The amount of points the player scores per 90 minutes.
        self.pp90 = self._pp90()
        #: The player's current price.
        self.price = self._additional["now_cost"] / 10.0
        #: The amount of red cards the player has received.
        self.red_cards = self._additional["red_cards"]
        #: The amount of saves the player has made.
        self.saves = self._additional["saves"]
        #: The player's second name.
        self.second_name = self._additional["second_name"]
        #: The percentage of users the player is selected by.
        self.selected_by = float(self._additional["selected_by_percent"])
        #: The status of the player, which can be available, injured or ...
        self.status = self._additional["status"]
        #: The player's squad number.
        self.squad_number = self._additional["squad_number"]
        #: The ID of the team the player plays for.
        self.team_id = self._additional["team"]
        #: The team the player currently plays for.
        self.team = team_converter(self.team_id)
        #: The player's transfers in in the current season.
        self.transfers_in = self._additional["transfers_in"]
        #: The player's transfers out in the current season.
        self.transfers_out = self._additional["transfers_out"]
        #: The amount of yellow cards the player has received.
        self.yellow_cards = self._additional["yellow_cards"]

    def _get_specific(self):
        """
        Returns the player with the specific player_id.
        """
        return requests.get(
            "{}element-summary/{}".format(API_BASE_URL, self._id)).json()

    def _games_played(self):
        """
        Returns the amount of games a player has played in.
        """
        return sum([1 for fixture in self.fixtures if fixture["minutes"] > 0])

    def _pp90(self):
        """
        Returns the amount of points a player scores per 90 minutes played.
        """
        if self.minutes == 0:
            return 0
        return self.points / float(self.minutes)

    def __str__(self):
        return "{} - {} - {}".format(self.name, self.position, self.team)
