Team
================

.. module:: fpl

Information for the :class:`Team <fpl.models.team.Team>` is taken from the following endpoint:

    https://fantasy.premierleague.com/api/teams

An example of what information a :class:`Team <fpl.models.team.Team>` (Manchester United) contains is shown below:

.. code-block:: javascript

  {
    "id": 14,
    "current_event_fixture": [
      {
        "is_home": true,
        "month": 1,
        "event_day": 1,
        "id": 226,
        "day": 19,
        "opponent": 3
      }
    ],
    "next_event_fixture": [
      {
        "is_home": true,
        "month": 1,
        "event_day": 1,
        "id": 235,
        "day": 29,
        "opponent": 4
      }
    ],
    "name": "Man Utd",
    "code": 1,
    "short_name": "MUN",
    "unavailable": false,
    "strength": 4,
    "position": 0,
    "played": 0,
    "win": 0,
    "loss": 0,
    "draw": 0,
    "points": 0,
    "form": null,
    "link_url": "",
    "strength_overall_home": 1280,
    "strength_overall_away": 1290,
    "strength_attack_home": 1250,
    "strength_attack_away": 1260,
    "strength_defence_home": 1310,
    "strength_defence_away": 1340,
    "team_division": 1
  }

.. autoclass:: fpl.models.team.Team
   :members:
