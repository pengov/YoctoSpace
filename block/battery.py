#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  battery.py
#
#  Copyright 2019 Nicolas Pengov <nicolas.pengov@sfr.fr>
#


#   ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~   IMPORT
import pymunkoptions
pymunkoptions.options["debug"] = False
import pymunk
from .model_block import ModelBlock
import pyglet
from random import random


#   ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~   CLASS
class Battery(ModelBlock):
    def __init__(self, pos_ship, space_ship, nothing=False):
        super(Battery, self).__init__(
                life=250,
                weight=2500,
                STORAGE_MAX=160,
                CRITICAl_LIFE=50,
                RECV_MAX=10,
                space_ship=space_ship,
                pos_ship=pos_ship,
                COST=50
                )

        self.RADIUS = 32 * 4.5
        self.SEND_MAX = 20

        if not nothing:
            moment = pymunk.moment_for_box(self.weight, (32, 32))
            body = pymunk.Body(self.weight, moment)
            shape = pymunk.Poly(body, [(-16, -16), (-16, 16), (16, 16), (16, -16)])
            self._set_body_shape(body, shape)

            temp = self.space_ship.sprites_creation[self.pos_ship[1]][self.pos_ship[0]][1].image
            if self.space_ship == self.space_ship.Var.main_space_ship:
                img = self.space_ship.Var.image["battery"].get_transform(flip_x=temp.flip_x, flip_y=temp.flip_y)
            else:
                img = self.space_ship.Var.image["battery"].get_transform(flip_x=temp.flip_x, flip_y=temp.flip_y)
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
        #   regarde les elements qu'il peut charger
        elements = []
        for line in objects:
            for element in line:
                if element:
                    if element.STORAGE_MAX >= 1 and "generator" not in repr(element) and element != self:
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
        if super(Battery, self).detect_critique():
            self.RADIUS = 32 * 4
            self.STORAGE_MAX = 100
            self.SEND_MAX = 15

    def help_info(self, consumption_label, label1, response_label1, label2, response_label2):
        consumption_label.text = "0"
        label1.text = "Radius:"
        response_label1.text = str(int(self.RADIUS / 32 - 0.5)) + " block"
        label2.text = ""
        response_label2.text = ""
