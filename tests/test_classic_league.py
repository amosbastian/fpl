import unittest

from fpl import FPL
from fpl.utils import _run


class ClassicLeagueTest(unittest.TestCase):
    def setUp(self):
        self.fpl = FPL()
        self.classic_league = _run(self.fpl.get_classic_league("633353"))

    def test_classic_league(self):
        self.assertEqual(
            self.classic_league.__str__(), "Steem Fantasy League - 633353")

    def test_get_standings(self):
        standings = _run(self.classic_league.get_standings(1))
        self.assertIsInstance(standings, dict)
        self.assertEqual(standings["results"][0]["rank"], 1)

if __name__ == '__main__':
    unittest.main()
