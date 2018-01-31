import requests
import json

API_BASE_URL = "https://fantasy.premierleague.com/drf/"

class FPL():
    def user(self, user_id):
        """
        Returns a User object containing information about the user with the 
        given `user_id`.

        :param string user_id: A user's id
        """
        return User(user_id)

    @property
    def teams(self):
        """
        Returns a list of Team objects of the teams currently participating 
        in the Premier League.
        """
        response = requests.get("{}teams".format(API_BASE_URL)).json()
        return[Team(team) for team in response]

    @property
    def players(self):
        """
        Returns a list of information about all players currently playing for 
        teams in the Premier League.
        """
        return requests.get("{}elements".format(API_BASE_URL)).json()

    def player(self, player_id):
        """
        Returns a Player object of the player with the given `player_id`.

        :param int player_id: A player's id
        """
        return Player(player_id)

    @property
    def gameweeks(self):
        """
        Returns a list Gameweek objects.
        """
        response = requests.get("{}events".format(API_BASE_URL)).json()
        return [Gameweek(gameweek) for gameweek in response]

    def gameweek(self, gameweek):
        """
        Returns a Gameweek object of the specified gameweek.

        :param int gameweek: The gameweek (1-38)
        """
        return self.gameweeks[gameweek - 1]

    @property
    def game_settings(self):
        """
        Returns a dictionary containing the Fantasy Premier League's rules.
        """
        return requests.get("{}game-settings".format(API_BASE_URL)).json()

    def classic_league(self, league_id):
        """
        Returns a ClassicLeague object from the given `league_id`.

        :param string league_id: A league's id
        """
        response = requests.get("{}leagues-classic-standings/{}".format(
            API_BASE_URL, league_id)).json()
        return ClassicLeague(response)

    def h2h_league(self, league_id):
        """
        Returns a H2HLeague object from the given `league_id`.

        :param string league_id: A league's id
        """
        response = requests.get("{}leagues-h2h-standings/{}".format(
            API_BASE_URL, league_id)).json()
        return H2HLeague(response)

if __name__ == '__main__':
    fpl = FPL()
    for player in fpl.classic_league(521697).standings["results"]:
        print(player["entry_name"], player["start_event"])