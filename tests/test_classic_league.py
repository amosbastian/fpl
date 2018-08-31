import unittest

from fpl import FPL


class ClassicLeagueTest(unittest.TestCase):
    def setUp(self):
        self.fpl = FPL()
        self.classic_league = self.fpl.get_classic_league("633353")

    def test_classic_league(self):
        self.assertEqual(
            self.classic_league.__str__(), "Steem Fantasy League - 633353")

    def test__get_information(self):
        information = self.classic_league._information
        self.assertIsInstance(information, dict)

    def test_get_standings(self):
        self.classic_league.get_standings()
        standings = self.classic_league.standings
        self.assertIsInstance(standings, list)
        self.assertEqual(standings[0]["rank"], 1)

if __name__ == '__main__':
    unittest.main()
