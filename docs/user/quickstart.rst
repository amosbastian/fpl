Quickstart
==========

This part of the user guide will try to make it a bit more easy for
users to get started with using `fpl`! Before starting, make sure that
`fpl` is :ref:`installed and up to date <installation>`.

Creating an FPL object
----------------------

The :class:`FPL` class is the main way you will be accessing information
from the Fantasy Premier League's API.

Begin by importing the :class:`FPL` class from `fpl`::

    >>> from fpl import FPL

Because `fpl` uses `aiohttp <https://aiohttp.readthedocs.io/en/stable/>`,
we must also import this and pass a `Client Session <https://docs.aiohttp.org/en/stable/client_advanced.html>`
as an argument to the `FPL` class. You can either create a session and pass it like this::

    >>> import aiohttp
    >>>
    >>> async def main():
    ...     session = aiohttp.ClientSession()
    ...     fpl = FPL(session)
            # ...
    ...     await session.close()

or use a session context manager::

    >>> async def main():
    ...     async with aiohttp.ClientSession as session:
    ...         fpl = FPL(session)
    ...         # ...

Now, let's try to get a player. For this example, let's get Manchester United's
star midfielder Paul Pogba (replace `# ...` with this code)::

    >>> player = await fpl.get_player(302)
    >>> print(player)
    Pogba - Midfielder - Man Utd

Now, we have a :class:`Player <fpl.models.Player>` object called ``player``. We can
get all the information we need from this object. For example, if we want his
points per game, or his total points, then we can simply do this::

    >>> print(player.points_per_game)
    5.7
    >>> print(player.total_points)
    113

Each of :class:`FPL <fpl.FPL>`'s functions include the argument ``return_json`` -
if you want to get a ``dict`` instead of e.g. a :class:`Player <fpl.models.Player>` object,
then you can simply do the following::

    >>> player = await fpl.get_player(302, return_json=True)
    >>> print(player["total_points"])
    113

Nice, right? However, one important thing was left out. Because ``fpl`` is
asynchronous, you must use ``asyncio`` to run the function::

    >>> import asyncio
    >>> asyncio.run(main())

