ClassicLeague
================

Information for the :class:`ClassicLeague` is taken from e.g. the following endpoint:

    https://fantasy.premierleague.com/drf/leagues-classic-standings/1137

An example of what information a :class:`ClassicLeague` contains is shown below:

.. code-block:: javascript

  {
    "new_entries": {
      "has_next": false,
      "number": 1,
      "results": [
        {
          "id": 42289277,
          "entry_name": "Atl\u00e9tico Alitera\u00e7\u00e3o",
          "player_first_name": "Liam",
          "player_last_name": "O`Brien",
          "joined_time": "2019-01-21T13:41:56Z",
          "entry": 2513270,
          "league": 1137
        },
        ...,
        {
          "id": 42313251,
          "entry_name": "restnowmywarrior",
          "player_first_name": "Daniel",
          "player_last_name": "Trudgill",
          "joined_time": "2019-01-23T11:44:00Z",
          "entry": 952466,
          "league": 1137
        }
      ]
    },
    "league": {
      "id": 1137,
      "leagueban_set": [

      ],
      "name": "Official \/r\/FantasyPL Classic League",
      "short_name": null,
      "created": "2018-07-05T15:01:19Z",
      "closed": false,
      "forum_disabled": false,
      "make_code_public": false,
      "rank": null,
      "size": null,
      "league_type": "x",
      "_scoring": "c",
      "reprocess_standings": false,
      "admin_entry": 3027,
      "start_event": 1
    },
    "standings": {
      "has_next": true,
      "number": 1,
      "results": [
        {
          "id": 34680858,
          "entry_name": "Vaulen Tigers",
          "event_total": 72,
          "player_name": "Tore Bj\u00f8rheim",
          "movement": "same",
          "own_entry": false,
          "rank": 1,
          "last_rank": 1,
          "rank_sort": 1,
          "total": 1580,
          "entry": 226251,
          "league": 1137,
          "start_event": 1,
          "stop_event": 38
        },
        ...,
        {
          "id": 22006870,
          "entry_name": "( \u0361\u00b0 \u035c\u0296 \u0361\u00b0)",
          "event_total": 65,
          "player_name": "Amos Bastian",
          "movement": "down",
          "own_entry": true,
          "rank": 2185,
          "last_rank": 1943,
          "rank_sort": 2192,
          "total": 1404,
          "entry": 3808385,
          "league": 1137,
          "start_event": 1,
          "stop_event": 38
        }
      ]
    },
    "update_status": 0
  }

.. module:: fpl

.. autoclass:: fpl.models.classic_league.ClassicLeague
   :members:
