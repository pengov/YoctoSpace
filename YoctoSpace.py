# -*- coding: utf-8 -*-
#
#  YoctoSpace.py
#
#  Copyright 2019 Nicolas Pengov <nicolas.pengov@sfr.fr>
#


"""
YoctoSpace.py is the python file who lunch the game YoctoSpace

Yoctospace is a spatial simulation game sandbox. The game consists of
 a single-player game with fights against artificial intelligence and
  an empty field for training and a multiplayer game where it is the players
   who host the game and fight each other until one of them is defeated.

A battle ends when all enemy ships are destroyed.
And for a ship to be destroyed, it must have its heart.
When the core is destroyed all the blocks of the ship, which are
still connected or drifting in space, are subsequently destroyed.
"""


if __name__ == "__main__":
    from main import yoctospace_game
    import sys
    yoctospace_game(*sys.argv)
