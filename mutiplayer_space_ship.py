#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  mutiplayer_space_ship.py
#
#  Copyright 2019 Nicolas Pengov <nicolas.pengov@sfr.fr>
#


#   ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~   IMPORT
from space_ship import SpaceShip


#   ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ CLASS
class MultiplayerSpaceShip(SpaceShip):
    def __init__(self, Var=None):
        super(MultiplayerSpaceShip, self).__init__(Var)
        self.reactor_x = 0
        self.reactor_y = 0
        self.shot_pos = 0, 0

    def update(self, dt):
        super(MultiplayerSpaceShip, self).update(dt)
        super(MultiplayerSpaceShip, self).mouv(self.reactor_x, self.reactor_y, dt)

    def mouv(self, x, y):
        self.reactor_x = x
        self.reactor_y = y
