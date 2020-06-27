#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  button.py
#
#  Copyright 2019 Nicolas Pengov <nicolas.pengov@sfr.fr>
#


#   ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~   IMPORT
import pyglet


#   ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~   CLASS
class Button:
    """
    Button class
    create a button graphically  in 2D
    the area of the button where he can be clicked is the relation beetween posision and image_off size
    if the button is pressed he call an action in a function set by Button.set_function
    """

    def __init__(self, pos, image_off, image_on, anchor=(None, None), batch=None, group=None):
        if anchor == (None, None):
            self.hitbox = pos + (pos[0] + image_off.width, pos[1] + image_off.height)
        else:
            if anchor[0] == "center":
                anchor[0] = image_off.width // 2
            if anchor[1] == "center":
                anchor[1] = image_off.height // 2

            self.hitbox = pos[0] - anchor[0],\
                pos[1] - anchor[1],\
                pos[0] - anchor[0] + image_off.width,\
                pos[1] - anchor[1] + image_off.height

            image_off = image_off.get_transform()
            image_on = image_on.get_transform()
            image_off.anchor_x = image_on.anchor_x = anchor[0]
            image_off.anchor_y = image_on.anchor_y = anchor[1]

        self.sprite = pyglet.sprite.Sprite(
                                image_off,
                                x=pos[0],
                                y=pos[1],
                                batch=batch,
                                group=group
                                )

        self.type_image = "off"
        self.image_off = image_off
        self.image_on = image_on

        self.function = None
        self.args = ()
        self.kwargs = {}

    def set_function(self, function, *args, **kwargs):
        self.function = function
        self.args = args
        self.kwargs = kwargs

    def click(self, pos):
        """test if the button is pressed"""

        #   if the button is pressed so we change the image of the button
        if self.sprite.visible:
            if self.hitbox[0] <= pos[0] <= self.hitbox[2] and self.hitbox[1] <= pos[1] <= self.hitbox[3]:
                self.sprite.image = self.image_on
                self.type_image = "on"

    def reset(self):
        """reset the state of the button if he was pressed"""

        if self.type_image == "on":
            self.sprite.image = self.image_off
            self.type_image = "off"
            if self.function:
                self.function(*self.args, **self.kwargs)
