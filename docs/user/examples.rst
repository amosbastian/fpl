.. _examples:

Examples
========

.. module:: fpl

It always helps to have examples of how to implement certain things. Hopefully
this page will help you if you are stuck on something, and need some inspiration.
If there are certain examples you think would be helpful to add to this page,
then don't hesitate to `create an issue <https://github.com/amosbastian/fpl/issues>`_
detailing it.


The league's best ...
---------------------

One of things that is most interesting to see is which players are performing
the best in certain metrics. For example, which players score the most points
per game, or which players have the most goals + assists. This is really easy
to implement using `fpl`!

.. code-block:: python

  import asyncio

  import aiohttp
  from prettytable import PrettyTable

  from fpl import FPL


  async def main():
      async with aiohttp.ClientSession() as session:
          fpl = FPL(session)
          players = await fpl.get_players()

      top_performers = sorted(
          players, key=lambda x: x.goals_scored + x.assists, reverse=True)

      player_table = PrettyTable()
      player_table.field_names = ["Player", "£", "G", "A", "G + A"]
      player_table.align["Player"] = "l"

      for player in top_performers[:10]:
          goals = player.goals_scored
          assists = player.assists
          player_table.add_row([player.web_name, f"£{player.now_cost / 10}",
                              goals, assists, goals + assists])

      print(player_table)

  if __name__ == "__main__":
      asyncio.run(main())

which outputs the following table::

    +------------+-------+----+----+-------+
    | Player     |   £   | G  | A  | G + A |
    +------------+-------+----+----+-------+
    | Salah      | £13.6 | 16 | 8  |   24  |
    | Hazard     | £11.0 | 10 | 10 |   20  |
    | Sterling   | £11.3 | 10 | 10 |   20  |
    | Kane       | £12.4 | 14 | 6  |   20  |
    | Aubameyang | £11.3 | 14 | 5  |   19  |
    | Sané       |  £9.7 | 8  | 11 |   19  |
    | Wilson     |  £6.5 | 10 | 8  |   18  |
    | Agüero     | £11.3 | 10 | 8  |   18  |
    | Lacazette  |  £9.3 | 8  | 8  |   16  |
    | Pogba      |  £8.7 | 8  | 8  |   16  |
    +------------+-------+----+----+-------+

Of course this can be done with any of a :class:`Player <fpl.models.player.Player>`'s
attributes, so just experiment!
