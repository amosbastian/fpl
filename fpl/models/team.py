import requests

from ..constants import API_URLS
from .player import Player


class Team():
    """A class representing a real team in the Fantasy Premier League."""
    def __init__(self, team_id):
        self._id = team_id
        self._information = self._get_information()

        #: The name of the team, e.g. "Arsenal".
        self.name = self._information["name"]
        #: The team's code.
        self.code = self._information["code"]
        #: The short name of the team, e.g. "ARS".
        self.short_name = self._information["short_name"]
        #: The team's unavailability.
        self.unavailable = self._information["unavailable"]
        #: Strength of the team.
        self.strength = self._information["strength"]
        #: The team's position in the table.
        self.position = self._information["position"]
        #: Amount of games played.
        self.played = self._information["played"]
        #: Amount of games won.
        self.won = self._information["win"]
        #: Amount of games lost.
        self.lost = self._information["loss"]
        #: Amount of games drawn.
        self.drawn = self._information["draw"]
        #: Amount of points.
        self.points = self._information["points"]
        #: The team's form.
        self.form = self._information["form"]
        #: Team's overall strength at home.
        self.strength_overall_home = self._information["strength_overall_home"]
        #: Team's overall strength away from home.
        self.strength_overall_away = self._information["strength_overall_away"]
        #: Team's attacking strength at home.
        self.strength_attack_home = self._information["strength_attack_home"]
        #: Team's attacking strength away from home.
        self.strength_attack_away = self._information["strength_attack_away"]
        #: Team's defensive strength at home.
        self.strength_defence_home = self._information["strength_defence_home"]
        #: Team's defensive strength away from home.
        self.strength_defence_away = self._information["strength_defence_away"]
        #: A dictionary with information about the team's current fixture.
        self.current_fixture = self._information["current_event_fixture"][0]
        #: A dictionary with information about the team's next fixture.
        self.next_fixture = self._information["next_event_fixture"][0]
        #: The team's players.
        self.players = None

    def get_players(self):
        """Sets the `players` property as a list of players that play for the
        team.
        """
        response = requests.get(API_URLS["players"])
        if response.status_code == 200:
            players = [Player(player["id"], player)
                       for player in response.json()
                       if player["team_code"] == self.code]
        self.players = players

    def _get_information(self):
        response = requests.get(API_URLS["teams"]).json()
        return response[self._id - 1]

    def __str__(self):
        return self.name
