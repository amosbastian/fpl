import json
import requests

API_BASE_URL = "https://fantasy.premierleague.com/drf/"

class Team(object):
    """
    A class representing a real team in the Fantasy Premier League.
    """
    def __init__(self, team_id):
        self.id = team_id
        self._information = self._information()

        #: The name of the team, e.g. "Arsenal".
        self.name = self._information["name"]
        #: The short name of the team, e.g. "ARS".
        self.short_name = self._information["short_name"]

        self.current_fixture = self._information["current_event_fixture"][0]
        """
        A dictionary containing information about the team's current fixture.
        """
        self.next_fixture = self._information["next_event_fixture"][0]
        """
        A dictionary containing information about the team's next fixture.
        """

    def _information(self):
        response = requests.get("{}teams".format(API_BASE_URL)).json()
        return response[self.id - 1]

    def __str__(self):
        return self.name

if __name__ == '__main__':
    team = Team(1)
    print(team.next_fixture)