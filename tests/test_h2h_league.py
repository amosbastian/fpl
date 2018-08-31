import unittest

from fpl import FPL


class H2HLeagueTest(unittest.TestCase):
    def setUp(self):
        self.fpl = FPL()
        self.fpl.login()
        self.h2h_league = self.fpl.get_h2h_league("760869")

    def test_h2h_league(self):
        self.assertEqual(
            self.h2h_league.__str__(), "League 760869 - 760869")

    def test__get_information(self):
        information = self.h2h_league._information
        self.assertIsInstance(information, dict)

    def test_get_standings(self):
        self.h2h_league.get_fixtures()
        fixtures = self.h2h_league.fixtures
        self.assertIsInstance(fixtures, list)
        self.assertEqual(fixtures[0]["event"], 1)

if __name__ == '__main__':
    unittest.main()
