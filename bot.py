#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  bot.py
#
#  Copyright 2019 Nicolas Pengov <nicolas.pengov@sfr.fr>
#


#   ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~   IMPORT
from math import acos, pi, radians


#   ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~   CLASS
class Bot:
    def __init__(self, space_ship):
        self.space_ship = space_ship

    def step(self, dt):
        """call in the game loop
        establishes the actions to be done by the bot in a given case"""

        Var = self.space_ship.Var
        if Var.main_space_ship.objects[Var.main_space_ship.pos_core[1]][Var.main_space_ship.pos_core[0]] is None:
            self.space_ship.mouv(0, 0, dt)
            self.space_ship.stop_shot_cannon()
            self.space_ship.stop_shot_turret()
            return

        pos = self.space_ship.get_pos()
        pos_player = Var.main_space_ship.get_pos()
        angle = (0.5 * pi - radians(self.space_ship.get_angle())) % (2 * pi)
        angle -= 2 * pi if angle > pi else 0
        angle_ = angle
        velo, angu_velo = self.get_speed()
        velo_direct = (velo[0] ** 2 + velo[1] ** 2) ** 0.5

        delta_pos = ((pos_player[0] - pos[0]) ** 2 + (pos_player[1] - pos[1]) ** 2) ** 0.5
        delta_angle = abs(acos((pos_player[0] - pos[0]) / delta_pos))
        delta_angle *= (-1 if pos_player[1] - pos[1] < 0 else 1)

        if delta_angle < 0:
            delta_angle += 2 * pi
        elif delta_angle > 2 * pi:
            delta_angle -= 2 * pi
        if angle_ < 0:
            angle_ += 2 * pi
        elif angle_ > 2 * pi:
            angle_ -= 2 * pi

        delta_angle -= angle_
        if delta_angle > pi:
            delta_angle -= 2 * pi
        elif delta_angle <= -pi:
            delta_angle += 2 * pi

        #   action bot
        x, y = 0, 0

        if abs(angu_velo) > pi / 5:
            x = -1 if angu_velo < 0 else 1
        elif abs(delta_angle) > pi / 5:
            x = -1 if delta_angle > 0 else 1
        elif abs(delta_angle) > pi / 10:
            if abs(angu_velo) > pi / 10:
                x = -1 if angu_velo < 0 else 1
            else:
                x = -1 if delta_angle > 0 else 1
        elif abs(delta_angle) > pi / 20:
            if abs(angu_velo) > pi / 20:
                x = -1 if angu_velo < 0 else 1
            else:
                x = -1 if delta_angle > 0 else 1

        if velo_direct > 128:
            if angle - pi/5 < acos(velo[0] / velo_direct * (-1 if velo[1] < 0 else 1)) < angle + pi/5:
                y = -1
            elif angle - pi/5 < acos(velo[0] / velo_direct * (1 if velo[1] < 0 else -1)) < angle + pi/5:
                y = 1
        elif delta_pos > 512:
            if abs(delta_angle) < pi / 5:
                y = 1
            elif abs(delta_angle) > 2 * pi / 3:
                y = -1
        elif delta_pos > 256:
            if velo_direct > 48:
                if angle - pi/10 < acos(velo[0] / velo_direct * (-1 if velo[1] < 0 else 1)) < angle + pi/10:
                    y = -1
                elif angle - pi/10 < acos(velo[0] / velo_direct * (1 if velo[1] < 0 else -1)) < angle + pi/10:
                    y = 1
            elif abs(delta_angle) < pi / 10:
                y = 1
            elif abs(delta_angle) > 4 * pi / 5:
                y = -1
        elif delta_pos < 256:
            if abs(delta_angle) < pi / 5:
                y = -1
            elif abs(delta_angle) > 4 * pi / 5:
                y = 1

        if abs(delta_angle) < pi/10:
            self.space_ship.shot_cannon()
        else:
            self.space_ship.stop_shot_cannon()
        if delta_pos < 640:
            self.space_ship.shot_turret(shot_pos=pos_player)
        else:
            self.space_ship.stop_shot_turret()
        if abs(delta_angle) < pi / 5:
            self.space_ship.shot_torpedo(pos=pos_player)

        self.space_ship.mouv(x, y, dt)

    def get_speed(self) -> tuple:
        """getter function for the spoeed of the ship
        ship speed is the velocity of the core"""

        core = self.space_ship.objects[self.space_ship.pos_core[1]][self.space_ship.pos_core[0]]
        if core:
            return (core.body.velocity, core.body.angular_velocity)
        else:
            return ((0, 0), 0)
