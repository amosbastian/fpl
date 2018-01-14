python-fpl
==========

A Python wrapper around the Fantasy Premier League API.

Installing python-fpl
=====================

The recommended way to install fpl-python is via ``pip``.

.. code-block:: bash

   pip install fpl

.. note:: Depending on your system, you may need to use ``pip3`` to install
          packages for python 3.

Usage
-----

```python
import fpl
fpl = fpl.FPL()
```

Documentation
-------------

1. Get specific user

```python
print(fpl.user("3523615"))
```

2. Get specific user's history

```python
print(fpl.user_history("3523615"))
```

3. Get specific user's picks

```python
print(fpl.user_picks("3523615"))
```

4. Get specific user's cup information

```python
print(fpl.user_cup("3523615"))
```

5. Get specific user's transfers

```python
print(fpl.user_transfers("3523615"))
```

6. Get specific user's entered leagues

```python
print(fpl.user_leagues_entered("3523615"))
```

7. Get teams

```python
print(fpl.teams)
```

8. Get players

```python
print(fpl.players)
```

9. Get specific player

```python
print(fpl.player("123"))
```

10. Get gameweeks

```python
print(fpl.gameweeks)
```

11. Get specific gameweek

```python
print(fpl.gameweek(20))
```

12. Get game settings

```python
print(fpl.game_settings)
```

13. Get specific classic league information

```python
print(fpl.classic_league("743038"))
```

14. Get specific h2h league information

```python
print(fpl.h2h_league("28281"))
```
