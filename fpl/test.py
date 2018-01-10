import unittest
import fpl
class FPLTest(unittest.TestCase):
	def setUp(self):
		self.fantasypl = fpl.FPL()

	def test_user(self):
		user = self.fantasypl.user("3523615")
		self.assertEqual(isinstance(user, dict), True)

	def test_user_history(self):
		user_history = self.fantasypl.user_history("3523615")
		self.assertEqual(isinstance(user_history, dict), True)

	def test_user_picks(self):
		user_picks = self.fantasypl.user_picks("3523615", 20)
		self.assertEqual(isinstance(user_picks, dict), True)

	def test_user_cup(self):
		user_cup = self.fantasypl.user_cup("3523615")
		self.assertEqual(isinstance(user_cup, dict), True)

	def test_user_transfers(self):
		user_transfers = self.fantasypl.user_transfers("3523615")
		self.assertEqual(isinstance(user_transfers, dict), True)

	def test_user_leagues_entered(self):
		user_leagues_entered = self.fantasypl.user_leagues_entered("3523615")
		self.assertEqual(isinstance(user_leagues_entered, dict), True)

	def test_teams(self):
		teams = self.fantasypl.teams
		self.assertEqual(isinstance(teams, list), True)
		self.assertEqual(len(teams), 20)

	def test_players(self):
		players = self.fantasypl.players
		self.assertEqual(isinstance(players, list), True)
		self.assertEqual(len(players), players[-1]["id"])

	def test_player(self):
		player = self.fantasypl.player("123")
		self.assertEqual(isinstance(player, dict), True)

	def test_gameweeks(self):
		gameweeks = self.fantasypl.gameweeks
		self.assertEqual(isinstance(gameweeks, list), True)
		self.assertEqual(len(gameweeks), 38)

	def test_gameweek(self):
		gameweek = self.fantasypl.gameweek("20")
		self.assertEqual(isinstance(gameweek, dict), True)

	def test_game_settings(self):
		game_settings = self.fantasypl.game_settings
		self.assertEqual(isinstance(game_settings, dict), True)

	def test_classic_league(self):
		classic_league = self.fantasypl.classic_league("743038")
		self.assertEqual(isinstance(classic_league, dict), True)

	def test_h2h_league(self):
		h2h_league = self.fantasypl.h2h_league("28281")
		self.assertEqual(isinstance(h2h_league, dict), True)

if __name__ == '__main__':
	unittest.main()