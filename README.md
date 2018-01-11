# python-fpl

A Python wrapper around the Fantasy Premier League API.

# Installation

	pip install fpl

# Usage

	import fpl
	fpl = fpl.FPL()

# Documentation

1. Get specific user

	print(fpl.user("3523615"))

2. Get specific user's history

	print(fpl.user_history("3523615"))

3. Get specific user's picks

	print(fpl.user_picks("3523615"))

4. Get specific user's cup information

	print(fpl.user_cup("3523615"))

5. Get specific user's transfers

	print(fpl.user_transfers("3523615"))

6. Get specific user's entered leagues

print(fpl.user_leagues_entered("3523615"))

7. Get teams

	print(fpl.teams)

8. Get players

	print(fpl.players)

9. Get specific player

	print(fpl.player("123"))

10. Get gameweeks

	print(fpl.gameweeks)

11. Get specific gameweek

	print(fpl.gameweek(20))

12. Get game settings

	print(fpl.game_settings)

13. Get specific classic league information

	print(fpl.classic_league("743038"))

14. Get specific h2h league information

	print(fpl.h2h_league("28281"))