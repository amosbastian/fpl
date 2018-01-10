import requests
import json

API_BASE_URL = "https://fantasy.premierleague.com/drf/"

class FPL():
	def user(self, user_id):
		return requests.get("{}entry/{}".format(API_BASE_URL, user_id)).json()

	def user_history(self, user_id):
		return requests.get("{}entry/{}/history".format(API_BASE_URL,
			user_id)).json()

	def user_picks(self, user_id, gameweek):
		return requests.get("{}entry/{}/event/{}/picks".format(API_BASE_URL,
			user_id, gameweek)).json()

	def user_cup(self, user_id):
		return requests.get("{}entry/{}/cup".format(API_BASE_URL,
			user_id)).json()

	def user_transfers(self, user_id):
		return requests.get("{}entry/{}/transfers".format(API_BASE_URL,
			user_id)).json()

	def user_leagues_entered(self, user_id):
		return requests.get("{}leagues-entered/{}".format(API_BASE_URL,
			user_id)).json()

	@property
	def teams(self):
		return requests.get("{}teams".format(API_BASE_URL)).json()

	@property
	def players(self):
		return requests.get("{}elements".format(API_BASE_URL)).json()

	def player(self, player_id):
		return requests.get("{}element-summary/{}".format(API_BASE_URL,
			player_id)).json()

	@property
	def gameweeks(self):
		return requests.get("{}events".format(API_BASE_URL)).json()

	def gameweek(self, gameweek):
		return requests.get("{}event/{}/live".format(API_BASE_URL,
			gameweek)).json()

	@property
	def game_settings(self):
		return requests.get("{}game-settings".format(API_BASE_URL)).json()

	def classic_league(self, league_id):
		return requests.get("{}leagues-classic-standings/{}".format(
			API_BASE_URL, league_id)).json()

	def h2h_league(self, league_id):
		return requests.get("{}leagues-h2h-standings/{}".format(
			API_BASE_URL, league_id)).json()

if __name__ == '__main__':
	fpl = FPL()

	print(fpl.user("3523615"))