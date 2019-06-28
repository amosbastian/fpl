Player
================

.. module:: fpl

Information for the :class:`Player <fpl.models.player.Player>` is taken from e.g. the following endpoints:

    https://fantasy.premierleague.com/api/elements
    https://fantasy.premierleague.com/api/element-summary/1 (optional)

The information from the latter endpoint is only included when ``include_summary`` is ``True``.

An example of what information a :class:`Player <fpl.models.player.Player>` (Petr Cech) contains is shown below (without summary included):

.. code-block:: javascript

  {
    "id": 1,
    "photo": "11334.jpg",
    "web_name": "Cech",
    "team_code": 3,
    "status": "a",
    "code": 11334,
    "first_name": "Petr",
    "second_name": "Cech",
    "squad_number": 1,
    "news": "",
    "now_cost": 48,
    "news_added": "2018-09-29T17:31:14Z",
    "chance_of_playing_this_round": 100,
    "chance_of_playing_next_round": 100,
    "value_form": "0.0",
    "value_season": "5.0",
    "cost_change_start": -2,
    "cost_change_event": 0,
    "cost_change_start_fall": 2,
    "cost_change_event_fall": 0,
    "in_dreamteam": false,
    "dreamteam_count": 0,
    "selected_by_percent": "1.2",
    "form": "0.0",
    "transfers_out": 130119,
    "transfers_in": 81105,
    "transfers_out_event": 644,
    "transfers_in_event": 122,
    "loans_in": 0,
    "loans_out": 0,
    "loaned_in": 0,
    "loaned_out": 0,
    "total_points": 24,
    "event_points": 0,
    "points_per_game": "3.4",
    "ep_this": "0.0",
    "ep_next": "1.0",
    "special": false,
    "minutes": 585,
    "goals_scored": 0,
    "assists": 0,
    "clean_sheets": 1,
    "goals_conceded": 9,
    "own_goals": 0,
    "penalties_saved": 0,
    "penalties_missed": 0,
    "yellow_cards": 0,
    "red_cards": 0,
    "saves": 27,
    "bonus": 3,
    "bps": 130,
    "influence": "205.0",
    "creativity": "0.0",
    "threat": "0.0",
    "ict_index": "20.4",
    "ea_index": 0,
    "element_type": 1,
    "team": 1
  }

.. autoclass:: fpl.models.player.Player
   :members:
