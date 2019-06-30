from fpl.models.fixture import Fixture

fixture_data = {
    "id": 6,
    "kickoff_time_formatted": "10 Aug 20:00",
    "started": True,
    "event_day": 1,
    "deadline_time": "2018-08-10T18:00:00Z",
    "deadline_time_formatted": "10 Aug 19:00",
    "stats": [
        {
            "goals_scored": {
                "a": [{"value": 1, "element": 234}],
                "h": [{"value": 1, "element": 286}, {"value": 1, "element": 302}],
            }
        },
        {
            "assists": {
                "a": [{"value": 1, "element": 221}],
                "h": [{"value": 1, "element": 295}, {"value": 1, "element": 297}],
            }
        },
        {"own_goals": {"a": [], "h": []}},
        {"penalties_saved": {"a": [], "h": []}},
        {"penalties_missed": {"a": [], "h": []}},
        {
            "yellow_cards": {
                "a": [{"value": 1, "element": 226}],
                "h": [{"value": 1, "element": 304}, {"value": 1, "element": 481}],
            }
        },
        {"red_cards": {"a": [], "h": []}},
        {
            "saves": {
                "a": [{"value": 4, "element": 213}],
                "h": [{"value": 3, "element": 282}],
            }
        },
        {
            "bonus": {
                "a": [{"value": 1, "element": 234}],
                "h": [{"value": 3, "element": 286}, {"value": 2, "element": 302}],
            }
        },
        {
            "bps": {
                "a": [
                    {"value": 25, "element": 234},
                    {"value": 23, "element": 221},
                    {"value": 16, "element": 213},
                    {"value": 16, "element": 215},
                    {"value": 15, "element": 225},
                    {"value": 14, "element": 220},
                    {"value": 13, "element": 227},
                    {"value": 13, "element": 231},
                    {"value": 12, "element": 219},
                    {"value": 10, "element": 233},
                    {"value": 6, "element": 226},
                    {"value": 5, "element": 228},
                    {"value": 3, "element": 492},
                    {"value": 2, "element": 236},
                ],
                "h": [
                    {"value": 30, "element": 286},
                    {"value": 29, "element": 302},
                    {"value": 24, "element": 297},
                    {"value": 22, "element": 295},
                    {"value": 16, "element": 289},
                    {"value": 15, "element": 282},
                    {"value": 15, "element": 292},
                    {"value": 13, "element": 291},
                    {"value": 13, "element": 305},
                    {"value": 13, "element": 481},
                    {"value": 8, "element": 304},
                    {"value": 4, "element": 298},
                    {"value": 3, "element": 303},
                    {"value": -2, "element": 306},
                ],
            }
        },
    ],
    "team_h_difficulty": 3,
    "team_a_difficulty": 4,
    "code": 987597,
    "kickoff_time": "2018-08-10T19:00:00Z",
    "team_h_score": 2,
    "team_a_score": 1,
    "finished": True,
    "minutes": 90,
    "provisional_start_time": False,
    "finished_provisional": True,
    "event": 1,
    "team_a": 11,
    "team_h": 14,
}


class TestFixture(object):
    @staticmethod
    def test_init():
        fixture = Fixture(fixture_data)
        for k, v in fixture_data.items():
            assert getattr(fixture, k) == v

    @staticmethod
    def _do_test_not_finished(fixture, method):
        delattr(fixture, "finished")
        data_dict = getattr(fixture, method)()
        assert isinstance(data_dict, dict)
        assert len(data_dict) == 0

    @staticmethod
    def _do_test_finished(fixture, method):
        data_dict = getattr(fixture, method)()
        assert isinstance(data_dict, dict)
        assert len(data_dict) == 2

    def test_get_goalscorers_not_finished(self, fixture):
        self._do_test_not_finished(fixture, "get_goalscorers")

    def test_get_goalscorers_finished(self, fixture):
        self._do_test_finished(fixture, "get_goalscorers")

    def test_get_assisters_not_finished(self, fixture):
        self._do_test_not_finished(fixture, "get_assisters")

    def test_get_assisters_finished(self, fixture):
        self._do_test_finished(fixture, "get_assisters")

    def test_get_own_goalscorers_not_finished(self, fixture):
        self._do_test_not_finished(fixture, "get_own_goalscorers")

    def test_get_own_goalscorers_finished(self, fixture):
        self._do_test_finished(fixture, "get_own_goalscorers")

    def test_get_yellow_cards_not_finished(self, fixture):
        self._do_test_not_finished(fixture, "get_yellow_cards")

    def test_get_yellow_cards(self, fixture):
        self._do_test_finished(fixture, "get_yellow_cards")

    def test_get_red_cards_not_finished(self, fixture):
        self._do_test_not_finished(fixture, "get_red_cards")

    def test_get_red_cards_finished(self, fixture):
        self._do_test_finished(fixture, "get_red_cards")

    def test_get_penalty_saves_not_finished(self, fixture):
        self._do_test_not_finished(fixture, "get_penalty_saves")

    def test_get_penalty_saves_finished(self, fixture):
        self._do_test_finished(fixture, "get_penalty_saves")

    def test_get_penalty_misses_not_finished(self, fixture):
        self._do_test_not_finished(fixture, "get_penalty_misses")

    def test_get_penalty_misses_finished(self, fixture):
        self._do_test_finished(fixture, "get_penalty_misses")

    def test_get_saves_not_finished(self, fixture):
        self._do_test_not_finished(fixture, "get_saves")

    def test_get_saves_finished(self, fixture):
        self._do_test_finished(fixture, "get_saves")

    def test_get_bonus_not_finished(self, fixture):
        self._do_test_not_finished(fixture, "get_bonus")

    def test_get_bonus_finished(self, fixture):
        self._do_test_finished(fixture, "get_bonus")

    def test_get_bps_not_finished(self, fixture):
        self._do_test_not_finished(fixture, "get_bps")

    def test_get_bps_finished(self, fixture):
        self._do_test_finished(fixture, "get_bps")

    @staticmethod
    def test_str(fixture):
        assert str(fixture) == "Norwich vs. Man City - 10 Aug 19:00"
