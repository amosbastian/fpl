import unittest

from fpl import FPL


class UserTest(unittest.TestCase):
    def setUp(self):
        self.fpl = FPL()
        self.fpl.login()
        self.user = self.fpl.get_user("3808385")

    def test_history(self):
        history = self.user.history
        self.assertIsInstance(history, dict)

    def test_season_history(self):
        season_history = self.user.season_history
        self.assertIsInstance(season_history, list)

    def test_chips(self):
        chips = self.user.chips
        self.assertIsInstance(chips, list)

    def test_leagues(self):
        leagues = self.user.leagues
        self.assertIsInstance(leagues, dict)

    def test_classic(self):
        classic = self.user.classic
        self.assertIsInstance(classic, list)

    def test_h2h(self):
        h2h = self.user.h2h
        self.assertIsInstance(h2h, list)

    def test_picks(self):
        picks = self.user.picks
        self.assertIsInstance(picks, dict)

    def test_my_team(self):
        my_team = self.user.my_team()
        self.assertIsInstance(my_team, list)

    def test_team(self):
        team = self.user.team()
        self.assertIsInstance(team, list)
        team = self.user.team(gameweek=1)
        self.assertIsInstance(team, list)

    def test_chip(self):
        chip = self.user.chip()
        self.assertIsInstance(chip, list)
        chip = self.user.chip(gameweek=1)
        self.assertEqual(chip, "")

    def test_automatic_substitutions(self):
        automatic_substitutions = self.user.automatic_substitutions()
        self.assertIsInstance(automatic_substitutions, list)
        automatic_substitutions = self.user.automatic_substitutions(gameweek=1)
        self.assertIsInstance(automatic_substitutions, list)

    def test_gameweek_history(self):
        gameweek_history = self.user.gameweek_history()
        self.assertIsInstance(gameweek_history, list)
        gameweek_history = self.user.gameweek_history(gameweek=1)
        self.assertIsInstance(gameweek_history, dict)

    def test_transfers(self):
        transfers = self.user.transfers
        self.assertIsInstance(transfers, dict)

    def test_wildcards(self):
        wildcards = self.user.wildcards
        self.assertIsInstance(wildcards, list)

    def test_transfer_history(self):
        transfer_history = self.user.transfer_history()
        self.assertIsInstance(transfer_history, list)
        transfer_history = self.user.transfer_history(gameweek=1)
        self.assertIsInstance(transfer_history, list)

    def test_watchlist(self):
        watchlist = self.user.watchlist
        self.assertIsInstance(watchlist, list)

if __name__ == '__main__':
    unittest.main()
