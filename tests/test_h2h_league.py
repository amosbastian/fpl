import unittest

from fpl import FPL
from fpl.utils import _run


class H2HLeagueTest(unittest.TestCase):
    def setUp(self):
        self.fpl = FPL()
        _run(self.fpl.login())
        self.h2h_league = _run(self.fpl.get_h2h_league("760869"))

    def test_h2h_league(self):
        self.assertEqual(
            self.h2h_league.__str__(), "League 760869 - 760869")

    def test_fixtures(self):
        fixtures = _run(self.h2h_league.get_fixtures())
        self.assertIsInstance(fixtures, list)
        self.assertIsInstance(fixtures[0], dict)

if __name__ == '__main__':
    unittest.main()
