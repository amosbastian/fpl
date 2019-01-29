.. _examples:

Examples
========

.. module:: fpl

It always helps to have examples of how to implement certain things. Hopefully
this page will help you if you are stuck on something, and need some inspiration.
If there are certain examples you think would be helpful to add to this page,
then don't hesitate to `create an issue <https://github.com/amosbastian/fpl/issues>`_
detailing it.

.. note:: There is no doubt that the below examples could be implemented in a
          much better way - if you want to improve them, then don't hestitate to!

The league's best ...
---------------------

One of things that is most interesting to see is which players are performing
the best in certain metrics. For example, which players score the most points
per game, or which players have the most goals + assists. This is really easy
to implement using **fpl**!

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


Alternative FDR
---------------

As we all know, the official FDR used by the Fantasy Premier League is not the
best. With this in mind the function :meth:`FDR() <fpl.FPL.FDR>` was created,
which returns a dictionary containing an alternative FDR based on points
scored for / against teams! Using this dictionary we can create a table
containing each team's new FDR, which can then be used to decide which players
you should play the next gameweek. Below an example of this table with colour
highlighting is shown::

    import asyncio

    import aiohttp
    from colorama import Fore, init
    from prettytable import PrettyTable

    from fpl import FPL


    async def main():
        async with aiohttp.ClientSession() as session:
            fpl = FPL(session)
            fdr = await fpl.FDR()

        fdr_table = PrettyTable()
        fdr_table.field_names = [
            "Team", "All (H)", "All (A)", "GK (H)", "GK (A)", "DEF (H)", "DEF (A)",
            "MID (H)", "MID (A)", "FWD (H)", "FWD (A)"]

        for team, positions in fdr.items():
            row = [team]
            for difficulties in positions.values():
                for location in ["H", "A"]:
                    if difficulties[location] == 5.0:
                        row.append(Fore.RED + "5.0" + Fore.RESET)
                    elif difficulties[location] == 1.0:
                        row.append(Fore.GREEN + "1.0" + Fore.RESET)
                    else:
                        row.append(f"{difficulties[location]:.2f}")

            fdr_table.add_row(row)

        fdr_table.align["Team"] = "l"
        print(fdr_table)

    if __name__ == '__main__':
        asyncio.run(main())


which outputs the following table::


    +----------------+---------+---------+--------+--------+---------+---------+---------+---------+---------+---------+
    | Team           | All (H) | All (A) | GK (H) | GK (A) | DEF (H) | DEF (A) | MID (H) | MID (A) | FWD (H) | FWD (A) |
    +----------------+---------+---------+--------+--------+---------+---------+---------+---------+---------+---------+
    | Man City       |   4.45  |   5.0   |  3.62  |  5.0   |   3.75  |   5.0   |   4.61  |   5.0   |   5.0   |   3.94  |
    | Chelsea        |   3.99  |   3.47  |  3.72  |  3.01  |   3.62  |   3.35  |   4.01  |   3.93  |   4.09  |   4.42  |
    | West Ham       |   2.87  |   1.83  |  2.45  |  2.70  |   2.89  |   2.34  |   3.08  |   1.19  |   2.95  |   4.17  |
    | Cardiff        |   1.0   |   1.62  |  1.09  |  3.24  |   1.0   |   2.53  |   1.0   |   1.0   |   3.37  |   2.57  |
    | Newcastle      |   2.54  |   1.66  |  1.56  |  2.62  |   2.05  |   1.54  |   2.80  |   2.66  |   4.43  |   3.22  |
    | Everton        |   2.85  |   3.41  |  1.96  |  4.16  |   2.92  |   3.88  |   3.49  |   3.20  |   2.26  |   2.93  |
    | Watford        |   3.59  |   2.52  |  4.09  |  3.70  |   3.34  |   3.14  |   3.79  |   2.85  |   3.09  |   1.0   |
    | Fulham         |   1.09  |   1.48  |  1.81  |  2.17  |   1.16  |   2.32  |   1.77  |   1.26  |   1.26  |   2.78  |
    | Leicester      |   3.57  |   2.74  |  3.87  |  2.34  |   3.68  |   3.07  |   3.38  |   2.95  |   3.09  |   3.81  |
    | Crystal Palace |   3.08  |   1.41  |  3.16  |  1.0   |   3.22  |   1.0   |   3.18  |   2.87  |   2.55  |   4.37  |
    | Liverpool      |   4.91  |   4.66  |  4.32  |  4.76  |   5.0   |   4.63  |   4.10  |   4.08  |   4.53  |   5.0   |
    | Wolves         |   3.20  |   2.34  |  2.15  |  3.62  |   3.06  |   2.82  |   3.74  |   1.42  |   2.82  |   4.14  |
    | Bournemouth    |   1.75  |   3.30  |  1.86  |  3.93  |   2.29  |   3.40  |   2.00  |   3.69  |   1.34  |   3.23  |
    | Spurs          |   5.0   |   3.17  |  5.0   |  3.10  |   4.85  |   3.21  |   5.0   |   3.85  |   3.09  |   3.40  |
    | Man Utd        |   3.94  |   3.21  |  3.78  |  2.84  |   4.49  |   3.63  |   3.25  |   3.06  |   3.44  |   3.79  |
    | Huddersfield   |   2.19  |   1.0   |  1.37  |  2.16  |   2.60  |   1.34  |   3.05  |   2.04  |   1.0   |   2.08  |
    | Southampton    |   2.11  |   2.03  |  1.0   |  3.01  |   2.30  |   2.37  |   2.56  |   1.80  |   2.42  |   3.70  |
    | Burnley        |   1.57  |   2.41  |  1.63  |  4.18  |   1.86  |   2.61  |   2.04  |   2.02  |   1.65  |   3.71  |
    | Brighton       |   2.24  |   3.39  |  2.53  |  4.18  |   1.97  |   3.61  |   2.34  |   3.61  |   3.53  |   2.96  |
    | Arsenal        |   3.44  |   4.29  |  4.11  |  4.39  |   3.67  |   4.34  |   3.35  |   4.07  |   2.51  |   4.21  |
    +----------------+---------+---------+--------+--------+---------+---------+---------+---------+---------+---------+

Optimal captain choice?!
------------------------

One of the most important aspects of the Fantasy Premier League is your captain
choice each week. Of course, it's very difficult to get this correct each week!
Because of this, it's quite interesting (or frustrating) to see what could've been.
The code snippet below shows how you can create a table showing your captain and
top scorer of each gameweek, and their respective difference in points scored::

    import asyncio
    from operator import attrgetter

    import aiohttp
    from prettytable import PrettyTable

    from fpl import FPL
    from fpl.utils import team_converter


    def get_gameweek_score(player, gameweek):
        gameweek_history = next(history for history in player.history
                                if history["round"] == gameweek)
        return gameweek_history["total_points"]


    def get_gameweek_opponent(player, gameweek):
        gameweek_history = next(history for history in player.history
                                if history["round"] == gameweek)
        return (f"{team_converter(gameweek_history['opponent_team'])} ("
                f"{'H' if gameweek_history['was_home'] else 'A'})")


    def get_point_difference(player_a, player_b, gameweek):
        if player_a == player_b:
            return 0

        history_a = next(history for history in player_a.history
                        if history["round"] == gameweek)
        history_b = next(history for history in player_b.history
                        if history["round"] == gameweek)

        return history_a["total_points"] - history_b["total_points"]

    async def main(user_id):
        player_table = PrettyTable()
        player_table.field_names = ["Gameweek", "Captain", "Top scorer", "Δ"]
        player_table.align = "r"
        total_difference = 0

        async with aiohttp.ClientSession() as session:
            fpl = FPL(session)
            user = await fpl.get_user(user_id)
            picks = await user.get_picks()

            for i, elements in enumerate(picks):
                gameweek = i + 1
                captain_id = next(player for player in elements
                                  if player["is_captain"])["element"]
                players = await fpl.get_players(
                    [player["element"] for player in elements],
                    include_summary=True)

                captain = next(player for player in players
                              if player.id == captain_id)

                top_scorer = max(
                    players, key=lambda x: get_gameweek_score(x, gameweek))

                point_difference = get_point_difference(
                    captain, top_scorer, gameweek)

                player_table.add_row([
                    gameweek,
                    (f"{captain.web_name} - "
                    f"{get_gameweek_score(captain, gameweek)} points vs. "
                    f"{get_gameweek_opponent(captain, gameweek)}"),
                    (f"{top_scorer.web_name} - "
                    f"{get_gameweek_score(top_scorer, gameweek)} points vs. "
                    f"{get_gameweek_opponent(top_scorer, gameweek)}"),
                    point_difference
                ])

                total_difference += point_difference

        print(player_table)
        print(f"Total point difference is {abs(total_difference)} points!")

    if __name__ == '__main__':
        asyncio.run(main(3808385))

which outputs the following table::

    +----------+------------------------------------------+-------------------------------------------+-----+
    | Gameweek |                                  Captain |                                Top scorer |   Δ |
    +----------+------------------------------------------+-------------------------------------------+-----+
    |        1 |     Sánchez - 5 points vs. Leicester (H) |         Mané - 16 points vs. West Ham (H) | -11 |
    |        2 |  Agüero - 20 points vs. Huddersfield (H) |   Agüero - 20 points vs. Huddersfield (H) |   0 |
    |        3 |         Agüero - 2 points vs. Wolves (A) |     Robertson - 9 points vs. Brighton (H) |  -7 |
    |        4 |      Agüero - 6 points vs. Newcastle (H) |    Hazard - 11 points vs. Bournemouth (H) |  -5 |
    |        5 |         Agüero - 7 points vs. Fulham (H) |        Hazard - 20 points vs. Cardiff (H) | -13 |
    |        6 |        Agüero - 6 points vs. Cardiff (A) |  Wan-Bissaka - 9 points vs. Newcastle (H) |  -3 |
    |        7 |       Agüero - 8 points vs. Brighton (H) |      Hazard - 10 points vs. Liverpool (H) |  -2 |
    |        8 |          Kane - 1 points vs. Cardiff (H) |    Hazard - 14 points vs. Southampton (A) | -13 |
    |        9 |      Sterling - 0 points vs. Burnley (H) |         Mendy - 10 points vs. Burnley (H) | -10 |
    |       10 |     Robertson - 0 points vs. Cardiff (H) |          Mané - 15 points vs. Cardiff (H) | -15 |
    |       11 | Sterling - 21 points vs. Southampton (H) |  Sterling - 21 points vs. Southampton (H) |   0 |
    |       12 |           Mané - 3 points vs. Fulham (H) |      Robertson - 12 points vs. Fulham (H) |  -9 |
    |       13 |    Sterling - 16 points vs. West Ham (A) |     Sterling - 16 points vs. West Ham (A) |   0 |
    |       14 |  Sterling - 9 points vs. Bournemouth (H) |   Sterling - 9 points vs. Bournemouth (H) |   0 |
    |       15 |          Sané - 7 points vs. Watford (A) |   Fraser - 12 points vs. Huddersfield (H) |  -5 |
    |       16 |        Kane - 1 points vs. Leicester (A) | Robertson - 11 points vs. Bournemouth (A) | -10 |
    |       17 |          Kane - 5 points vs. Burnley (H) |       Hazard - 13 points vs. Brighton (A) |  -8 |
    |       18 |   Sané - 2 points vs. Crystal Palace (H) |          Kane - 15 points vs. Everton (A) | -13 |
    |       19 |      Kane - 6 points vs. Bournemouth (H) |        Hazard - 15 points vs. Watford (A) |  -9 |
    |       20 |           Kane - 6 points vs. Wolves (H) |     Pogba - 18 points vs. Bournemouth (H) | -12 |
    |       21 |    Hazard - 3 points vs. Southampton (H) |        Fraser - 12 points vs. Watford (H) |  -9 |
    |       22 |       Salah - 11 points vs. Brighton (A) |     Digne - 12 points vs. Bournemouth (H) |  -1 |
    |       23 | Salah - 15 points vs. Crystal Palace (H) |  Salah - 15 points vs. Crystal Palace (H) |   0 |
    +----------+------------------------------------------+-------------------------------------------+-----+
    Total point difference is 155 points!
