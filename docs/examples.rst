Examples
========

Printing information about a user
---------------------------------

To print the name, region and rank of a user we can simply do the following

.. code-block:: python

    from fpl.user import User

    user = User(3523615)

    print("Name:\t{} {}\nRegion:\t{}\nRank:\t{}".format(user.first_name,
        user.second_name, user.region_name, user.overall_rank))

which outputs

.. code-block:: none

    Name:   Amos Bastian
    Region: Netherlands
    Rank:   100243

Printing a list of the top 10 goalscorers
-----------------------------------------

If we want to find out the top goalscorers we can simply create a dictionary of 
`player_id`s with the amount of goals scored and then sort it, as follows

.. code-block:: python

    from fpl import FPL
    from fpl.player import Player

    fpl = FPL()

    players = fpl.get_players()

    for player in sorted(players, key=lambda x: x.goals, reverse=True)[:10]:
        print("{0:10} - {1:2} goals".format(player.name, player.goals))

with example output:

.. code-block:: none

    Kane       - 21 goals
    Salah      - 19 goals
    Agüero     - 17 goals
    Sterling   - 14 goals
    Vardy      - 11 goals
    Firmino    - 11 goals
    Lukaku     - 11 goals
    Rooney     - 10 goals
    Morata     - 10 goals
    Lacazette  -  9 goals

