Fixture
================

Information for the :class:`Fixture` is taken from e.g. the following endpoints:

    https://fantasy.premierleague.com/drf/fixtures/
    https://fantasy.premierleague.com/drf/fixtures/?event=1

An example of what information a :class:`Fixture` contains is shown below:

.. code-block:: javascript

  {
    "id": 6,
    "kickoff_time_formatted": "10 Aug 20:00",
    "started": true,
    "event_day": 1,
    "deadline_time": "2018-08-10T18:00:00Z",
    "deadline_time_formatted": "10 Aug 19:00",
    "stats": [...],
    "team_h_difficulty": 3,
    "team_a_difficulty": 4,
    "code": 987597,
    "kickoff_time": "2018-08-10T19:00:00Z",
    "team_h_score": 2,
    "team_a_score": 1,
    "finished": true,
    "minutes": 90,
    "provisional_start_time": false,
    "finished_provisional": true,
    "event": 1,
    "team_a": 11,
    "team_h": 14
  }

.. autoclass:: fpl.models.fixture.Fixture
   :members:
