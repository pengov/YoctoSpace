#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  reactor.py
#
#  Copyright 2019 Nicolas Pengov <nicolas.pengov@sfr.fr>
#


#   ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~   IMPORT
import pymunkoptions
pymunkoptions.options["debug"] = False
import pymunk
from .model_block import ModelBlock
import pyglet


#   ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~   CLASS
class Reactor(ModelBlock):
    def __init__(self, pos_ship, space_ship, nothing=False):
        super(Reactor, self).__init__(
                life=500,
                weight=250,
                STORAGE_MAX=1,
                CRITICAL_LIFE=300,
                RECV_MAX=2,
                space_ship=space_ship,
                pos_ship=pos_ship,
                COST=30
                )

        self.THRUST = 400_000
        self.CONSUMPTION = 1
        self.len_width = 1

        if not nothing:
            temp = self.space_ship.sprites_creation[self.pos_ship[1]][self.pos_ship[0]][1].image
            self.flip_y = temp.flip_y

            coo = [(-16, 0), (-16, 16), (16, 16), (16, 0)]
            if temp.flip_y:
                for i, element in enumerate(coo):
                    coo[i] = element[0], -element[1]

            moment = pymunk.moment_for_box(self.weight, (16, 32))
            body = pymunk.Body(self.weight, moment)
            shape = pymunk.Poly(body, coo)
            self._set_body_shape(body, shape)

            self.img_on = self.space_ship.Var.image["reactor"].get_transform(flip_x=temp.flip_x, flip_y=temp.flip_y)
            self.img_off = self.space_ship.Var.image["reactor off"].get_transform(flip_x=temp.flip_x, flip_y=temp.flip_y)
            self.img_on.anchor_x = self.img_on.width // 2
            self.img_on.anchor_y = self.img_on.height // 2
            self.img_off.anchor_x = self.img_off.width // 2
            self.img_off.anchor_y = self.img_off.height // 2

            self.sprite = pyglet.sprite.Sprite(
                            self.img_off,
                            x=self.pos[0],
                            y=self.pos[1],
                            batch=self.space_ship.batch,
                            group=self.space_ship.z0
                            )

    def _init_(self):
        top = False
        if self.pos_ship[1] != len(self.space_ship.objects) - 1:
            element_top = self.space_ship.sprites_creation[self.pos_ship[1] + 1][self.pos_ship[0]]
            if element_top[0]:
                if not element_top[0] in ("triangular block", "reactor", "cannon", "torpedo launch"):
                    top = True
                elif element_top[0] == "triangular block":
                    if not element_top[1].image.flip_y:
                        top = True
                elif element_top[0] == "reactor":
                    if element_top[1].image.flip_y:
                        top = True
                elif element_top[0] == "torpedo launch":
                    if not element_top[1].image.flip_y:
                        top = True

        bottom = False
        left = False
        right = False

        self._set_joint_side(top, bottom, left, right)

    def init_pos(self, space_ship_pos, side, len_width, len_height):
        super(Reactor, self).init_pos(space_ship_pos, side, len_width, len_height)
        self.len_width = len_width

    def propulse(self, x, y, dt):
        THRUST = self.THRUST
        if self.storage > self.CONSUMPTION * dt and (x or y):
            self.sprite.image = self.img_on
            self.storage -= self.CONSUMPTION * dt
            if y == 1:
                if not self.flip_y:
                    self.body.apply_force_at_local_point((0, THRUST), (0, 0))
                else:
                    self.body.apply_force_at_local_point((0, THRUST // 2), (0, 0))
            elif y == -1:
                THRUST = -self.THRUST
                if not self.flip_y:
                    self.body.apply_force_at_local_point((0, THRUST // 2), (0, 0))
                else:
                    self.body.apply_force_at_local_point((0, THRUST), (0, 0))

            if x == 1:
                self.body.apply_force_at_local_point((0, THRUST), (-16 * THRUST // self.THRUST, 16))
            elif x == -1:
                self.body.apply_force_at_local_point((0, THRUST), (16 * THRUST // self.THRUST, 16))
            if self.space_ship.Var.sfx:
                self.space_ship.Var.music["sfx"]["reactor"].play()
        else:
            self.sprite.image = self.img_off

    def detect_critique(self):
        if super(Reactor, self).detect_critique():
            self.THRUST = 100_000

    def help_info(self, consumption_label, label1, response_label1, label2, response_label2):
        consumption_label.text = str(self.CONSUMPTION)
        label1.text = ""
        response_label1.text = ""
        label2.text = ""
        response_label2.text = ""
