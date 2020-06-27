#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  cannon.py
#
#  Copyright 2019 Nicolas Pengov <nicolas.pengov@sfr.fr>
#


#   ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~   IMPORT
import pymunkoptions
pymunkoptions.options["debug"] = False
import pymunk
from .model_block import ModelBlock
import pyglet
from bullet import CannonBullet
from math import cos, sin, pi


#   ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~   CLASS
class Cannon(ModelBlock):
    def __init__(self, pos_ship, space_ship, nothing=False):
        super(Cannon, self).__init__(
                life=500,
                weight=1000,
                STORAGE_MAX=5,
                RECV_MAX=3,
                space_ship=space_ship,
                pos_ship=pos_ship,
                COST=60
                )

        self._shot = False
        self.RELOADING = 0.25
        self.reloading = 0
        self.ENERGY_PER_SHOT = 1

        if not nothing:
            temp = self.space_ship.sprites_creation[self.pos_ship[1]][self.pos_ship[0]][1].image

            coo = [(-8, -16), (-8, 42), (16, 42), (16, -16)]
            if temp.flip_x:
                for i in range(len(coo)):
                    coo[i] = coo[i][0] * -1, coo[i][1]
            if temp.flip_y:
                for i in range(len(coo)):
                    coo[i] = coo[i][0], coo[i][1] * -1

            moment = pymunk.moment_for_box(self.weight, (24, 58))
            body = pymunk.Body(self.weight, moment)
            shape = pymunk.Poly(body, coo)
            self._set_body_shape(body, shape)

            img = self.space_ship.Var.image["cannon"].get_transform(flip_x=temp.flip_x, flip_y=temp.flip_y)
            img.anchor_x = img.width // 2
            img.anchor_y = img.height // 4 if not temp.flip_y else img.height // 4 * 3

            self.sprite = pyglet.sprite.Sprite(
                            img,
                            x=self.pos[0],
                            y=self.pos[1],
                            batch=self.space_ship.batch,
                            group=self.space_ship.z0
                            )

    def _init_(self):
        image = self.space_ship.sprites_creation[self.pos_ship[1]][self.pos_ship[0]][1].image
        top = False
        bottom = False

        left = False
        if image.flip_x:
            if self.pos_ship[0] != 0:
                element_left = self.space_ship.sprites_creation[self.pos_ship[1]][self.pos_ship[0] - 1]
                if element_left[0]:
                    if not element_left[0] in ("triangular block", "reactor", "cannon", "torpedo launch"):
                        left = True
                    elif element_left[0] == "triangular block":
                        if element_left[1].image.flip_x:
                            left = True
                    elif element_left[0] == "cannon":
                        if not element_left[1].image.flip_x:
                            left = True

        right = False
        if not image.flip_x:
            if self.pos_ship[0] != len(self.space_ship.objects[0]) - 1:
                element_right = self.space_ship.sprites_creation[self.pos_ship[1]][self.pos_ship[0] + 1]
                if element_right[0]:
                    if not element_right[0] in ("triangular block", "reactor", "cannon", "torpedo launch"):
                        right = True
                    elif element_right[0] == "triangular block":
                        if not element_right[1].image.flip_x:
                            right = True
                    elif element_right[0] == "cannon":
                        if element_right[1].image.flip_x:
                            right = True

        self._set_joint_side(top, bottom, left, right)

    def shot(self):
        self._shot = True

    def stop_shot(self):
        self._shot = False

    def update(self, dt):
        if self._shot:
            self.reloading += dt
            if self.reloading >= self.RELOADING:
                if self.storage >= self.ENERGY_PER_SHOT:
                    self.reloading = 0
                    self.storage -= self.ENERGY_PER_SHOT
                    flip_y = self.space_ship.sprites_creation[self.pos_ship[1]][self.pos_ship[0]][1].image.flip_y
                    angle = self.body.angle + pi if flip_y else self.body.angle
                    pos = self.get_pos()
                    pos = pos[0] + sin(-angle) * 64, pos[1] + cos(-angle) * 64
                    if self.space_ship.Var.sfx:
                        self.space_ship.Var.music["sfx"]["cannon shot"].play()
                    CannonBullet(angle, pos, self.space_ship)

    def help_info(self, consumption_label, label1, response_label1, label2, response_label2):
        consumption_label.text = str(self.ENERGY_PER_SHOT) + "/shot"
        label1.text = "Reload:"
        response_label1.text = str(self.RELOADING) + "s"
        label2.text = "Damage:"
        response_label2.text = str(CannonBullet.DAMAGE)
