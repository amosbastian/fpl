import unittest

from fpl import FPL
from fpl.utils import _run


class UserTest(unittest.TestCase):
    def setUp(self):
        self.fpl = FPL()
        _run(self.fpl.login())
        self.user = _run(self.fpl.get_user("3808385"))

    def test_gameweek_history(self):
        history = _run(self.user.get_gameweek_history())
        self.assertIsInstance(history, list)

        history = _run(self.user.get_gameweek_history(1))
        self.assertIsInstance(history, dict)

    def test_season_history(self):
        season_history = _run(self.user.get_season_history())
        self.assertIsInstance(season_history, list)

    def test_chips_history(self):
        chips = _run(self.user.get_chips_history())
        self.assertIsInstance(chips, list)

    def test_leagues(self):
        leagues = self.user.leagues
        self.assertIsInstance(leagues, dict)

    def test_picks(self):
        picks = _run(self.user.get_picks())
        self.assertIsInstance(picks, list)
        self.assertEqual(len(picks), self.user.current_event)

        picks = _run(self.user.get_picks(1))
        self.assertIsInstance(picks, list)

    def test_active_chips(self):
        active_chips = _run(self.user.get_active_chips())
        self.assertIsInstance(active_chips, list)
        self.assertEqual(len(active_chips), self.user.current_event)

        active_chips = _run(self.user.get_active_chips(1))
        self.assertIsInstance(active_chips, list)

    def test_automatic_substitutions(self):
        automatic_substitutions = _run(self.user.get_automatic_substitutions())
        self.assertIsInstance(automatic_substitutions, list)
        self.assertEqual(len(automatic_substitutions),
                         self.user.current_event)

        automatic_substitutions = _run(
            self.user.get_automatic_substitutions(1))
        self.assertIsInstance(automatic_substitutions, list)

    def test_team(self):
        my_team = _run(self.user.get_team())
        self.assertIsInstance(my_team, list)

    def test_transfers(self):
        transfers = _run(self.user.get_transfers())
        self.assertIsInstance(transfers, list)

        transfers = _run(self.user.get_transfers(1))
        self.assertIsInstance(transfers, list)

    def test_wildcards(self):
        wildcards = _run(self.user.get_wildcards())
        self.assertIsInstance(wildcards, list)

    def test_watchlist(self):
        watchlist = _run(self.user.get_watchlist())
        self.assertIsInstance(watchlist, list)

if __name__ == '__main__':
    unittest.main()
