User
================

Information for the :class:`User` is taken from the following endpoint:

    https://fantasy.premierleague.com/drf/entry/3808385

An example of what information a :class:`User` contains is shown below:

.. code-block:: javascript

  {
    "entry": {
      "id": 3808385,
      "player_first_name": "Amos",
      "player_last_name": "Bastian",
      "player_region_id": 152,
      "player_region_name": "Netherlands",
      "player_region_short_iso": "NL",
      "summary_overall_points": 1404,
      "summary_overall_rank": 49225,
      "summary_event_points": 65,
      "summary_event_rank": 1480275,
      "joined_seconds": 18267,
      "current_event": 23,
      "total_transfers": 21,
      "total_loans": 0,
      "total_loans_active": 0,
      "transfers_or_loans": "transfers",
      "deleted": false,
      "email": false,
      "joined_time": "2018-08-09T22:44:21Z",
      "name": "( \u0361\u00b0 \u035c\u0296 \u0361\u00b0)",
      "bank": 22,
      "value": 1037,
      "kit": "{\"kit_shirt_type\":\"plain\",\"kit_shirt_base\":\"#ff0000\",\"kit_shirt_sleeves\":\"#ff0000\",\"kit_shirt_secondary\":\"#e1e1e1\",\"kit_shirt_logo\":\"none\",\"kit_shorts\":\"#000000\",\"kit_socks_type\":\"plain\",\"kit_socks_base\":\"#ffffff\",\"kit_socks_secondary\":\"#e1e1e1\"}",
      "event_transfers": 0,
      "event_transfers_cost": 0,
      "extra_free_transfers": 0,
      "strategy": null,
      "favourite_team": 14,
      "started_event": 1,
      "player": 7425806
    },
    "leagues": {
      "cup": [

      ],
      "h2h": [

      ],
      "classic": [
        {
          "id": 14,
          "entry_rank": 8454,
          "entry_last_rank": 7255,
          "entry_movement": "down",
          "entry_change": 1199,
          "entry_can_leave": false,
          "entry_can_admin": false,
          "entry_can_invite": false,
          "entry_can_forum": false,
          "entry_code": null,
          "name": "Man Utd",
          "short_name": "team-14",
          "created": "2018-07-05T12:12:23Z",
          "closed": false,
          "forum_disabled": false,
          "make_code_public": false,
          "rank": null,
          "size": null,
          "league_type": "s",
          "_scoring": "c",
          "reprocess_standings": false,
          "admin_entry": null,
          "start_event": 1
        },
        ...,
        {
          "id": 890172,
          "entry_rank": 2,
          "entry_last_rank": 2,
          "entry_movement": "same",
          "entry_change": null,
          "entry_can_leave": true,
          "entry_can_admin": false,
          "entry_can_invite": false,
          "entry_can_forum": true,
          "entry_code": null,
          "name": "AJ's Angels",
          "short_name": null,
          "created": "2018-08-10T08:15:37Z",
          "closed": false,
          "forum_disabled": false,
          "make_code_public": false,
          "rank": null,
          "size": null,
          "league_type": "x",
          "_scoring": "c",
          "reprocess_standings": false,
          "admin_entry": 9346,
          "start_event": 1
        }
      ]
    }
  }

.. autoclass:: fpl.models.user.User
   :members:
