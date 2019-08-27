class Gameweek():
    """A class representing a gameweek of the Fantasy Premier League.

    Basic usage::

      >>> from fpl import FPL
      >>> import aiohttp
      >>> import asyncio
      >>>
      >>> async def main():
      ...     async with aiohttp.ClientSession() as session:
      ...         fpl = FPL(session)
      ...         gameweek = await fpl.get_gameweek(1)
      ...     print(gameweek)
      ...
      >>> asyncio.run(main())
      Gameweek 1 - 10 Aug 19:00
    """
    def __init__(self, gameweek_information):
        for k, v in gameweek_information.items():
            setattr(self, k, v)

    def __str__(self):
        return f"{self.name}"
