from fpl.models.fixture import Fixture


class TestFixture(object):
    def test_init(self):
        data = {
            "id": 265,
            "kickoff_time_formatted": None,
            "started": False,
            "event_day": None,
            "deadline_time": None,
            "deadline_time_formatted": None,
            "stats": [],
            "team_h_difficulty": 2,
            "team_a_difficulty": 4,
            "code": 987856,
            "kickoff_time": None,
            "team_h_score": None,
            "team_a_score": None,
            "finished": False,
            "minutes": 0,
            "provisional_start_time": False,
            "finished_provisional": False,
            "event": None,
            "team_a": 3,
            "team_h": 6,
        }
        fixture = Fixture(data)
        for k, v in data.items():
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

    def test_str(self, fixture):
        assert str(fixture) == "Man Utd vs. Leicester - 10 Aug 19:00"
