class TestFixture(object):
    def test_get_goalscorers(self, loop, fixture):
        goalscorers = fixture.get_goalscorers()
        assert isinstance(goalscorers, dict)

    def test_get_assisters(self, loop, fixture):
        assisters = fixture.get_assisters()
        assert isinstance(assisters, dict)

    def test_get_own_goalscorers(self, loop, fixture):
        own_goalscorers = fixture.get_own_goalscorers()
        assert isinstance(own_goalscorers, dict)

    def test_get_yellow_cards(self, loop, fixture):
        yellow_cards = fixture.get_yellow_cards()
        assert isinstance(yellow_cards, dict)

    def test_get_red_cards(self, loop, fixture):
        red_cards = fixture.get_red_cards()
        assert isinstance(red_cards, dict)

    def test_get_penalty_saves(self, loop, fixture):
        penalty_saves = fixture.get_penalty_saves()
        assert isinstance(penalty_saves, dict)

    def test_get_penalty_misses(self, loop, fixture):
        penalty_misses = fixture.get_penalty_misses()
        assert isinstance(penalty_misses, dict)

    def test_get_saves(self, loop, fixture):
        saves = fixture.get_saves()
        assert isinstance(saves, dict)

    def test_get_bonus(self, loop, fixture):
        bonus = fixture.get_bonus()
        assert isinstance(bonus, dict)

    def test_get_bps(self, loop, fixture):
        bps = fixture.get_bps()
        assert isinstance(bps, dict)
