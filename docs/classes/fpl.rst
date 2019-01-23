FPL
================

The :class:`FPL` class is the main class used for interacting with Fantasy Premier League's API. It
requires a ``aiohttp.ClientSession`` for sending requests, so typical usage of the :class:`FPL` class
can look something like this:

.. code-block:: python

  import asyncio
  import aiohttp
  from fpl import FPL


  async def main():
      async with aiohttp.ClientSession() as session:
          fpl = FPL(session)
          await fpl.login()
          user = await fpl.get_user(3808385)
          my_team = await user.get_team()

      print(my_team)

  asyncio.run(main())

.. autoclass:: fpl.fpl.FPL
   :members:
