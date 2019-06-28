H2HLeague
================

Information for the :class:`H2HLeague <fpl.models.h2h_league.H2HLeague>` is taken from the following endpoints:

    https://fantasy.premierleague.com/api/leagues-h2h-standings/829116
    https://fantasy.premierleague.com/api/leagues-entries-and-h2h-matches/829116/?page=1

An example of what information a :class:`H2HLeague <fpl.models.h2h_league.H2HLeague>` contains is shown below:

.. code-block:: javascript

  {
    "new_entries": {
      "has_next": false,
      "number": 1,
      "results": [

      ]
    },
    "league": {
      "id": 829116,
      "leagueban_set": [

      ],
      "name": "League 829116",
      "has_started": true,
      "can_delete": false,
      "short_name": null,
      "created": "2018-08-09T18:10:37Z",
      "closed": true,
      "forum_disabled": false,
      "make_code_public": false,
      "rank": null,
      "size": null,
      "league_type": "c",
      "_scoring": "h",
      "ko_rounds": 2,
      "admin_entry": null,
      "start_event": 1
    },
    "standings": {
      "has_next": false,
      "number": 1,
      "results": [
        {
          "id": 1230859,
          "entry_name": "fcjeff",
          "player_name": "Khalid Jeffal",
          "movement": "same",
          "own_entry": false,
          "rank": 1,
          "last_rank": 1,
          "rank_sort": 1,
          "total": 0,
          "matches_played": 23,
          "matches_won": 16,
          "matches_drawn": 1,
          "matches_lost": 6,
          "points_for": 1330,
          "points_against": 0,
          "points_total": 49,
          "division": 141015,
          "entry": 21127
        },
        ...,
        {
          "id": 1230854,
          "entry_name": "Wilson-fc",
          "player_name": "Liam Wilson",
          "movement": "same",
          "own_entry": false,
          "rank": 20,
          "last_rank": 20,
          "rank_sort": 20,
          "total": 0,
          "matches_played": 23,
          "matches_won": 6,
          "matches_drawn": 1,
          "matches_lost": 16,
          "points_for": 1115,
          "points_against": 0,
          "points_total": 19,
          "division": 141015,
          "entry": 3649536
        }
      ]
    },
    "matches_next": {
      "has_next": false,
      "number": 1,
      "results": [
        {
          "id": 33164099,
          "entry_1_entry": 3651588,
          "entry_1_name": "subi",
          "entry_1_player_name": "subi ebrahim",
          "entry_2_entry": 3648783,
          "entry_2_name": "Baugveien FC",
          "entry_2_player_name": "Nina Simonsen",
          "is_knockout": false,
          "winner": null,
          "tiebreak": null,
          "own_entry": false,
          "entry_1_points": 0,
          "entry_1_win": 0,
          "entry_1_draw": 0,
          "entry_1_loss": 0,
          "entry_2_points": 0,
          "entry_2_win": 0,
          "entry_2_draw": 0,
          "entry_2_loss": 0,
          "entry_1_total": 0,
          "entry_2_total": 0,
          "seed_value": null,
          "event": 24
        },
        ...,
        {
          "id": 33164094,
          "entry_1_entry": 367548,
          "entry_1_name": "Spartans fc",
          "entry_1_player_name": "Shehryar Gaba",
          "entry_2_entry": 303318,
          "entry_2_name": "Red Devils",
          "entry_2_player_name": "Ajay Bhullar",
          "is_knockout": false,
          "winner": null,
          "tiebreak": null,
          "own_entry": false,
          "entry_1_points": 51,
          "entry_1_win": 1,
          "entry_1_draw": 0,
          "entry_1_loss": 0,
          "entry_2_points": 39,
          "entry_2_win": 0,
          "entry_2_draw": 0,
          "entry_2_loss": 1,
          "entry_1_total": 3,
          "entry_2_total": 0,
          "seed_value": null,
          "event": 23
        }
      ]
    }
  }

.. autoclass:: fpl.models.h2h_league.H2HLeague
   :members:
