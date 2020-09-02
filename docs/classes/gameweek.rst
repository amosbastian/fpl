Gameweek
================

Information for the :class:`Gameweek <fpl.models.gameweek.Gameweek>` is taken from e.g. the following endpoints:
  https://fantasy.premierleague.com/api/bootstrap-static/
  https://fantasy.premierleague.com/api/event/1/live


An example of part of what information a :class:`Gameweek <fpl.models.gameweek.Gameweek>` contains is shown below:

.. code-block:: javascript

  {
    "id": 1,
    "name": "Gameweek 1",
    "deadline_time": "2020-09-12T10:00:00Z",
    "average_entry_score": 0,
    "finished": false,
    "data_checked": false,
    "highest_scoring_entry": null,
    "deadline_time_epoch": 1599904800,
    "deadline_time_game_offset": 0,
    "highest_score": null,
    "is_previous": false,
    "is_current": false,
    "is_next": true,
    "chip_plays": [

    ],
    "most_selected": null,
    "most_transferred_in": null,
    "top_element": null,
    "top_element_info": null,
    "transfers_made": 0,
    "most_captained": null,
    "most_vice_captained": null
    }

This is only the information from the bootstrap-static endpoint - the information from the live endpoint is too large to show, so it is recommended that you
check that endpoint yourself to get an idea of what it contains.

Basic usage:

.. code-block:: python

  from fpl import FPL
  import aiohttp
  import asyncio
  
  async def main():
      async with aiohttp.ClientSession() as session:
          fpl = FPL(session)
          gameweek = await fpl.get_gameweek(1)
      print(gameweek)

  asyncio.get_event_loop().run_until_complete(main())
  # Gameweek 1 - Deadline Sat 12 Sep 10:00

.. autoclass:: fpl.models.gameweek.Gameweek
   :members:
