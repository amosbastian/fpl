Examples
========

Printing information about a user
---------------------------------

To print the name, region and rank of a user we can simply do the following

.. code-block:: python

    fpl = fpl.FPL()
    user = fpl.user("3523615")

    print("Name:\t{} {}\nRegion:\t{}\nRank:\t{}".format(
        user["entry"]["player_first_name"],
        user["entry"]["player_last_name"],
        user["entry"]["player_region_name"],
        user["entry"]["summary_overall_rank"]
    ))

which outputs

.. code-block:: default

    Name:   Amos Bastian
    Region: Netherlands
    Rank:   100243

Printing a list of the top 10 goalscorers
-----------------------------------------

If we want to find out the top goalscorers we can simply create a dictionary of 
`player_id`s with the amount of goals scored and then sort it, as follows

.. code-block:: python

    import fpl
    import json

    def build_form():
        """
        Returns dictionary with the amount of goals scored by each player.
        """
        player_form = {}

        for player in players:
            player_id = player["id"]
            goals_scored = player["goals_scored"]
            player_form[player_id] = goals_scored

        return player_form

    if __name__ == '__main__':
        fpl = fpl.FPL()
        players = fpl.players
        player_form = build_form()
        sorted_players = sorted(player_form.items(), key=lambda x:x[1],
            reverse=True)

        for player in sorted_players[:10]:
            print("Player with id {} has scored {} goals!".format(player[0],
                player[1]))

with example output:

.. code-block:: default

    Player with id 394 has scored 20 goals!
    Player with id 234 has scored 18 goals!
    Player with id 247 has scored 14 goals!
    Player with id 257 has scored 13 goals!
    Player with id 161 has scored 10 goals!
    Player with id 235 has scored 10 goals!
    Player with id 285 has scored 10 goals!
    Player with id 472 has scored 10 goals!
    Player with id 209 has scored 9 goals!
    Player with id 28 has scored 8 goals!
