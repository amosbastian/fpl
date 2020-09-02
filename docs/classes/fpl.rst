FPL
================

.. module:: fpl

The :class:`FPL <fpl.FPL>` class is the main class used for interacting with Fantasy Premier League's API. It
requires an ``aiohttp.ClientSession`` for sending requests, so typical usage of the :class:`FPL <fpl.FPL>` class
can look something like this:

.. code-block:: python

  import asyncio
  import aiohttp
  from fpl import FPL

  async def main():
      async with aiohttp.ClientSession() as session:
          fpl = FPL(session)
          await fpl.login()
          user = await fpl.get_user()
          my_team = await user.get_team()

      print(my_team)

  asyncio.get_event_loop().run_until_complete(main())

Note that when calling the ``login`` function, you must either specify an ``email`` and ``password``,
or set up system environment variables named ``FPL_EMAIL`` and ``FPL_PASSWORD``.

.. autoclass:: fpl.fpl.FPL
   :members:
