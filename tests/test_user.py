import unittest

from fpl import FPL
from fpl.utils import _run


class UserTest(unittest.TestCase):
    def setUp(self):
        self.fpl = FPL()
        _run(self.fpl.login())
        self.user = _run(self.fpl.get_user("3808385"))

    def test_history(self):
        history = _run(self.user.get_history())
        self.assertIsInstance(history, dict)

    def test_season_history(self):
        season_history = _run(self.user.get_season_history())
        self.assertIsInstance(season_history, list)

    def test_chips_history(self):
        chips = _run(self.user.get_chips_history())
        self.assertIsInstance(chips, list)

    def test_leagues(self):
        leagues = _run(self.user.get_leagues())
        self.assertIsInstance(leagues, dict)

    def test_classic(self):
        classic = _run(self.user.get_classic_leagues())
        self.assertIsInstance(classic, list)

    def test_h2h(self):
        h2h = _run(self.user.get_h2h_leagues())
        self.assertIsInstance(h2h, list)

    def test_picks(self):
        picks = _run(self.user.get_picks())
        self.assertIsInstance(picks, list)
        self.assertEqual(len(picks), self.user.current_gameweek)

    def test_my_team(self):
        my_team = _run(self.user.my_team())
        self.assertIsInstance(my_team, list)

    def test_team(self):
        team = _run(self.user.get_team())
        self.assertIsInstance(team, list)
        team = _run(self.user.get_team(gameweek=1))
        self.assertIsInstance(team, list)

    def test_chip(self):
        chip = _run(self.user.get_chips())
        self.assertIsInstance(chip, list)
        chip = _run(self.user.get_chips(gameweek=1))
        self.assertEqual(chip, "")

    def test_automatic_substitutions(self):
        automatic_substitutions = _run(self.user.get_automatic_substitutions())
        self.assertIsInstance(automatic_substitutions, list)
        automatic_substitutions = _run(
            self.user.get_automatic_substitutions(gameweek=1))
        self.assertIsInstance(automatic_substitutions, list)

    def test_gameweek_history(self):
        gameweek_history = _run(self.user.get_gameweek_history())
        self.assertIsInstance(gameweek_history, list)
        gameweek_history = _run(self.user.get_gameweek_history(gameweek=1))
        self.assertIsInstance(gameweek_history, dict)

    def test_transfers(self):
        transfers = _run(self.user.get_transfers())
        self.assertIsInstance(transfers, dict)

    def test_wildcards(self):
        wildcards = _run(self.user.get_wildcards())
        self.assertIsInstance(wildcards, list)

    def test_transfer_history(self):
        transfer_history = _run(self.user.get_transfer_history())
        self.assertIsInstance(transfer_history, list)
        transfer_history = _run(self.user.get_transfer_history(gameweek=1))
        self.assertIsInstance(transfer_history, list)

    def test_watchlist(self):
        watchlist = _run(self.user.get_watchlist())
        self.assertIsInstance(watchlist, list)

if __name__ == '__main__':
    unittest.main()
