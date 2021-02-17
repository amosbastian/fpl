Fixture
================

.. module:: fpl

Information for the :class:`Fixture <fpl.models.fixture.Fixture>` is taken from e.g. the following endpoints:
  https://fantasy.premierleague.com/api/fixtures/
  https://fantasy.premierleague.com/api/fixtures/?event=1

An example of what information a :class:`Fixture <fpl.models.fixture.Fixture>` contains is shown below:

.. code-block:: javascript

  {
    "code": 2128288,
    "event": 1,
    "finished": false,
    "finished_provisional": false,
    "id": 2,
    "kickoff_time": "2020-09-12T11:30:00Z",
    "minutes": 0,
    "provisional_start_time": false,
    "started": false,
    "team_a": 1,
    "team_a_score": null,
    "team_h": 8,
    "team_h_score": null,
    "stats": [

    ],
    "team_h_difficulty": 3,
    "team_a_difficulty": 2
  }

Basic usage:

.. code-block:: python

  from fpl import FPL
  import aiohttp
  import asyncio

  async def main():
      async with aiohttp.ClientSession() as session:
          fpl = FPL(session)
          fixture = await fpl.get_fixture(3)
      print(fixture)

  # Python 3.7+
  asyncio.run(main())
  ...
  # Python 3.6
  loop = asyncio.get_event_loop()
  loop.run_until_complete(main())
  
  # Liverpool vs. Leeds - Sat 12 Sep 16:30

.. autoclass:: fpl.models.fixture.Fixture
   :members:
