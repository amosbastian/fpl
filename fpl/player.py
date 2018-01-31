import json
import requests

API_BASE_URL = "https://fantasy.premierleague.com/drf/"

class Player(object):
    """
    A class representing a player in the Fantasy Premier League.
    """
    def __init__(self, player_id):
        self.id = player_id
        self._specific = self._specific()
        self._additional = self._additional()

        # Player names
        self.name = self._additional["web_name"]
        self.first_name = self._additional["first_name"]
        self.second_name = self._additional["second_name"]

        # Gameweek and transfer information
        self.gameweek_points = self._additional["event_points"]
        self.gameweek_price_change = self._additional["cost_change_event"]
        self.gameweek_transfers_in = self._additional["transfers_in_event"]
        self.gameweek_transfers_out = self._additional["transfers_out_event"]
        self.transfers_in = self._additional["transfers_in"]
        self.transfers_out = self._additional["transfers_out"]

        # General information
        self.price = self._additional["now_cost"] / 10.0
        self.goals = self._additional["goals_scored"]        
        self.assists = self._additional["assists"]
        self.clean_sheets = self._additional["clean_sheets"]
        self.saves = self._additional["saves"]
        self.ppg = self._additional["points_per_game"]
        self.minutes = self._additional["minutes"]
        self.bps = self._additional["bps"]
        self.penalties_missed = self._additional["penalties_missed"]
        self.yellow_cards = self._additional["yellow_cards"]
        self.red_cards = self._additional["red_cards"]
        self.selected_by = float(self._additional["selected_by_percent"])


    @property
    def status(self):
        """The status of the player, which can be available, injured or ..."""
        return self._additional["status"]

    @property
    def team(self):
        """Conveŕt team number to actual Team object"""
        return self._additional["team"]

    @property
    def position(self):
        """Convert number to actual position"""
        return self._additional["element_type"]

    @property
    def explain(self):
        return self._specific["explain"]

    @property
    def fixtures(self):
        return self._specific["fixtures"]

    @property
    def history_summary(self):
        return self._specific["history_summary"]

    @property
    def fixtures_summary(self):
        return self._specific["fixtures_summary"]

    @property
    def history_past(self):
        return self._specific["history_past"]

    @property
    def history(self):
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

if __name__ == '__main__':
    print(Player(1).name)