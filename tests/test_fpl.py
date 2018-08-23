import unittest
import warnings

from fpl import FPL
from fpl.models.classic_league import ClassicLeague
from fpl.models.gameweek import Gameweek
from fpl.models.h2h_league import H2HLeague
from fpl.models.player import Player
from fpl.models.team import Team
from fpl.models.user import User


class FPLTest(unittest.TestCase):
    def setUp(self):
        self.fpl = FPL()
        warnings.filterwarnings("ignore", category=ResourceWarning,
                                message="unclosed.*<ssl.SSLSocket.*>")

    def test_user(self):
        user = self.fpl.get_user("3523615")
        self.assertTrue(isinstance(user, User))

    def test_teams(self):
        teams = self.fpl.get_teams()
        self.assertEqual(isinstance(teams, list), True)
        self.assertEqual(len(teams), 20)

    def test_players(self):
        players = self.fpl.get_players()
        self.assertTrue(isinstance(players, list))
        self.assertTrue(isinstance(players[0], Player))

    def test_gameweeks(self):
        gameweeks = self.fpl.get_gameweeks()
        self.assertTrue(isinstance(gameweeks, list))
        self.assertEqual(len(gameweeks), 38)

    def test_gameweek(self):
        gameweek = self.fpl.get_gameweek("20")
        self.assertTrue(isinstance(gameweek, Gameweek))

    def test_game_settings(self):
        game_settings = self.fpl.game_settings()
        self.assertEqual(isinstance(game_settings, dict), True)

    def test_classic_league(self):
        classic_league = self.fpl.get_classic_league("890172")
        self.assertTrue(isinstance(classic_league, ClassicLeague))

    def test_h2h_league(self):
        h2h_league = self.fpl.get_h2h_league("760869")
        self.assertTrue(isinstance(h2h_league, H2HLeague))


if __name__ == '__main__':
    unittest.main()
