#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  generator.py
#
#  Copyright 2019 Nicolas Pengov <nicolas.pengov@sfr.fr>
#


#   ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~   IMPORT
import pymunkoptions
pymunkoptions.options["debug"] = False
import pymunk
from .model_block import ModelBlock
import pyglet
from pathfinding.core.grid import Grid
from pathfinding.finder.a_star import AStarFinder
from random import random


#   ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~   CLASS
class Generator(ModelBlock):
    def __init__(self, pos_ship, space_ship, nothing=False):
        super(Generator, self).__init__(
                life=500,
                weight=7500,
                STORAGE_MAX=40,
                CRITICAL_LIFE=200,
                space_ship=space_ship,
                pos_ship=pos_ship,
                COST=200
                )

        self.PRODUCTION = 8
        self.SEND_MAX = 20
        self.RADIUS = 32 * 3.5

        if not nothing:
            moment = pymunk.moment_for_box(self.weight, (32, 32))
            body = pymunk.Body(self.weight, moment)
            shape = pymunk.Poly(body, [(-16, -16), (-16, 16), (16, 16), (16, -16)])
            self._set_body_shape(body, shape)

            temp = self.space_ship.sprites_creation[self.pos_ship[1]][self.pos_ship[0]][1].image
            if self.space_ship == self.space_ship.Var.main_space_ship:
                img = self.space_ship.Var.image["generator"].get_transform(flip_x=temp.flip_x, flip_y=temp.flip_y)
            else:
                img = self.space_ship.Var.image["generator"].get_transform(flip_x=temp.flip_x, flip_y=temp.flip_y)
            img.anchor_x = img.width // 2
            img.anchor_y = img.height // 2

            self.sprite = pyglet.sprite.Sprite(
                            img,
                            x=self.pos[0],
                            y=self.pos[1],
                            batch=self.space_ship.batch,
                            group=self.space_ship.z0
                            )

    def update(self, dt, objects):
        #   calculates if it is connected to the generator with the A* algorithm
        #   if it's not connected then it doesn't do anything
        pos_core = self.space_ship.pos_core
        matrix = []
        for i in objects:
            matrix.append([])
            for j in i:
                if "triangular" not in repr(j) and\
                        "reactor" not in repr(j) and\
                        "cannon" not in repr(j) and\
                        "turret" not in repr(j) and\
                        "torpedo" not in repr(j) and\
                        j is not None:
                    matrix[-1].append(1)
                else:
                    matrix[-1].append(0)
        grid = Grid(matrix=matrix)
        start = grid.node(self.pos_ship[0], self.pos_ship[1])
        end = grid.node(pos_core[0], pos_core[1])
        finder = AStarFinder()
        if not finder.find_path(start, end, grid)[0]:
            return None

        self.storage = min(self.storage + self.PRODUCTION * dt, self.STORAGE_MAX)

        #   regarde les elements qu'il peut charger
        elements = []
        for line in objects:
            for element in line:
                if element:
                    if element.STORAGE_MAX >= 1 and "generator" not in repr(element):
                        if element.storage != element.STORAGE_MAX:
                            pos = element.get_pos()
                            self_pos = self.get_pos()
                            radius_ = ((pos[0] - self_pos[0]) ** 2 + (pos[1] - self_pos[1]) ** 2) ** 0.5
                            if radius_ < self.RADIUS:
                                elements.append((radius_, random(), element))
        elements.sort()
        for i, element in enumerate(elements):
            elements[i] = element[0], element[2]

        send = 0
        for r, element in elements:
            to_send = min(self.SEND_MAX * dt - send, self.storage, element.STORAGE_MAX - element.storage, element.RECV_MAX * dt)
            element.storage += to_send
            self.storage -= to_send
            send += to_send
            if send == self.SEND_MAX * dt or self.storage == 0:
                break

    def detect_critique(self):
        if super(Generator, self).detect_critique():
            self.PRODUCTION = 6
            self.STORAGE_MAX = 100
            self.SEND_MAX = 15

    def help_info(self, consumption_label, label1, response_label1, label2, response_label2):
        consumption_label.text = "0"
        label1.text = "Radius:"
        response_label1.text = str(int(self.RADIUS / 32 - 0.5)) + " block"
        label2.text = "Production:"
        response_label2.text = str(self.PRODUCTION) + "/s"
