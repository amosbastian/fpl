import unittest
from fpl import FPL


class FPLTest(unittest.TestCase):
    def setUp(self):
        self.fpl = FPL()

    def test_user(self):
        user = self.fpl.get_user("3523615")
        self.assertEqual(isinstance(user, dict), True)

    def test_teams(self):
        teams = self.fpl.get_teams()
        self.assertEqual(isinstance(teams, list), True)
        self.assertEqual(len(teams), 20)

    def test_players(self):
        players = self.fpl.get_players()
        self.assertEqual(isinstance(players, list), True)
        self.assertEqual(len(players), players[-1]["id"])

    def test_gameweeks(self):
        gameweeks = self.fpl.get_gameweeks()
        self.assertEqual(isinstance(gameweeks, list), True)
        self.assertEqual(len(gameweeks), 38)

    def test_gameweek(self):
        gameweek = self.fpl.get_gameweek("20")
        self.assertEqual(isinstance(gameweek, dict), True)

    def test_game_settings(self):
        game_settings = self.fpl.game_settings()
        self.assertEqual(isinstance(game_settings, dict), True)

    def test_classic_league(self):
        classic_league = self.fpl.get_classic_league("743038")
        self.assertEqual(isinstance(classic_league, dict), True)

    def test_h2h_league(self):
        h2h_league = self.fpl.get_h2h_league("28281")
        self.assertEqual(isinstance(h2h_league, dict), True)


if __name__ == '__main__':
    unittest.main()
