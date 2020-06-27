#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  main.py
#
#  Copyright 2019 Nicolas Pengov <nicolas.pengov@sfr.fr>
#


#   ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~   IMPORT
import pyglet
from variable import Var
from event import ScreenEvent
from pyglet.gl import glScalef


#   ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~   FUNCTION
def yoctospace_game(*args, **kwargs) -> int:
    """
    Main function that initializes and starts the game
    """

    #   initializes variables that don't have a constant value or are too heavy like images
    Var.init()

    #   configure the game window
    Var.screen.set_size(*Var.SCREEN_SIZE)
    Var.screen.set_caption(Var.CAPTION)
    Var.screen.set_fullscreen(Var.FULLSCREEN)
    Var.screen.set_mouse_visible(Var.MOUSE_VISIBLE)
    Var.screen.set_icon(Var.image["icon2"], Var.image["icon1"])
    glScalef(1.0, 1.0, 1.0)

    Var.background = pyglet.sprite.Sprite(Var.image["background"], x=0, y=0)
    #   initializes the party in charge of events
    #   it is at the end because it needs everything to be initialized before it can be initialized
    ScreenEvent(Var.screen, Var)
    Var.screen_event = ScreenEvent

    Var.set_scene("menu")
    pyglet.app.run()
    return 0


if __name__ == "__main__":
    import sys
    import os

    if os.name == "nt":
        yoctospace_game(*sys.argv)
    else:
        from tkinter.messagebox import showerror
        showerror("Error", "The game is currently only supported by windows.")
