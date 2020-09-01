Player
================

.. module:: fpl

Information for the :class:`Player <fpl.models.player.Player>` is taken from e.g. the following endpoints:

    https://fantasy.premierleague.com/api/bootstrap-static/
    https://fantasy.premierleague.com/api/element-summary/302/ (optional)

The information from the latter endpoint is only included when ``include_summary`` is ``True``.

An example of what information a :class:`Player <fpl.models.player.Player>` (Bruno Fernandes) contains is
shown below (without summary included):

.. code-block:: javascript

  {
    "chance_of_playing_next_round": null,
    "chance_of_playing_this_round": null,
    "code": 141746,
    "cost_change_event": 0,
    "cost_change_event_fall": 0,
    "cost_change_start": 0,
    "cost_change_start_fall": 0,
    "dreamteam_count": 0,
    "element_type": 3,
    "ep_next": "0.0",
    "ep_this": null,
    "event_points": 0,
    "first_name": "Bruno Miguel",
    "form": "0.0",
    "id": 302,
    "in_dreamteam": false,
    "news": "",
    "news_added": null,
    "now_cost": 105,
    "photo": "141746.jpg",
    "points_per_game": "8.4",
    "second_name": "Borges Fernandes",
    "selected_by_percent": "25.4",
    "special": false,
    "squad_number": null,
    "status": "a",
    "team": 13,
    "team_code": 1,
    "total_points": 117,
    "transfers_in": 0,
    "transfers_in_event": 0,
    "transfers_out": 0,
    "transfers_out_event": 0,
    "value_form": "0.0",
    "value_season": "11.1",
    "web_name": "Fernandes",
    "minutes": 1187,
    "goals_scored": 8,
    "assists": 8,
    "clean_sheets": 9,
    "goals_conceded": 6,
    "own_goals": 0,
    "penalties_saved": 0,
    "penalties_missed": 0,
    "yellow_cards": 2,
    "red_cards": 0,
    "saves": 0,
    "bonus": 18,
    "bps": 366,
    "influence": "551.8",
    "creativity": "479.3",
    "threat": "361.0",
    "ict_index": "139.2",
    "influence_rank": 94,
    "influence_rank_type": 30,
    "creativity_rank": 55,
    "creativity_rank_type": 43,
    "threat_rank": 93,
    "threat_rank_type": 50,
    "ict_index_rank": 72,
    "ict_index_rank_type": 42
  }

.. autoclass:: fpl.models.player.Player
   :members:
