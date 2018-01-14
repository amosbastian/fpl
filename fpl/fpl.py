import requests
import json

API_BASE_URL = "https://fantasy.premierleague.com/drf/"

class FPL():
    def user(self, user_id):
        """
        Returns the user with the given `user_id`
        """
        return requests.get("{}entry/{}".format(API_BASE_URL, user_id)).json()

    def user_history(self, user_id):
        """
        Returns the history of the user with the given `user_id`
        """
        return requests.get("{}entry/{}/history".format(API_BASE_URL,
            user_id)).json()

    def user_picks(self, user_id, gameweek):
        """
        Returns the picks of the user with the given `user_id` in the given
        gameweek
        """
        return requests.get("{}entry/{}/event/{}/picks".format(API_BASE_URL,
            user_id, gameweek)).json()

    def user_cup(self, user_id):
        """
        Returns information about the user with the given `user_id`'s cup
        progression
        """
        return requests.get("{}entry/{}/cup".format(API_BASE_URL,
            user_id)).json()

    def user_transfers(self, user_id):
        """
        Returns all transfers of the user with the given `user_id`
        """
        return requests.get("{}entry/{}/transfers".format(API_BASE_URL,
            user_id)).json()

    def user_leagues_entered(self, user_id):
        """
        Returns all leagues that the user with the given `user_id` is currently
        participating in
        """
        return requests.get("{}leagues-entered/{}".format(API_BASE_URL,
            user_id)).json()

    @property
    def teams(self):
        """
        Returns all teams currently participating in the Premier League
        """
        return requests.get("{}teams".format(API_BASE_URL)).json()

    @property
    def players(self):
        """
        Returns all players currently playing for teams in the Premier League
        """
        return requests.get("{}elements".format(API_BASE_URL)).json()

    def player(self, player_id):
        """
        Returns the player with the given `player_id`
        """
        return requests.get("{}element-summary/{}".format(API_BASE_URL,
            player_id)).json()

    @property
    def gameweeks(self):
        """
        Returns information about all the gameweeks
        """
        return requests.get("{}events".format(API_BASE_URL)).json()

    def gameweek(self, gameweek):
        """
        Returns information about the specified gameweek
        """
        return requests.get("{}event/{}/live".format(API_BASE_URL,
            gameweek)).json()

    @property
    def game_settings(self):
        """
        Returns information about the Fantasy Premier League's rules
        """
        return requests.get("{}game-settings".format(API_BASE_URL)).json()

    def classic_league(self, league_id):
        """
        Returns information about the classic league with the given `league_id`
        """
        return requests.get("{}leagues-classic-standings/{}".format(
            API_BASE_URL, league_id)).json()

    def h2h_league(self, league_id):
        """
        Returns information about the h2h league with the given `league_id`
        """
        return requests.get("{}leagues-h2h-standings/{}".format(
            API_BASE_URL, league_id)).json()

if __name__ == '__main__':
    fpl = FPL()

    print(fpl.user("3523615"))