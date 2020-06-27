#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  triangular_block.py
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
class TriangularBlock(ModelBlock):
    def __init__(self, pos_ship, space_ship, nothing=False):
        super(TriangularBlock, self).__init__(
                life=500,
                weight=500,
                space_ship=space_ship,
                pos_ship=pos_ship,
                COST=10
                )

        if not nothing:
            coo = [(0, 0), (0, 0), (0, 0)]
            image = self.space_ship.sprites_creation[self.pos_ship[1]][self.pos_ship[0]][1].image
            if not image.flip_y:
                coo[0] = -16, -16
                coo[2] = 16, -16
                if not image.flip_x:
                    coo[1] = -16, 16
                else:
                    coo[1] = 16, 16
            else:
                coo[0] = -16, 16
                coo[1] = 16, 16
                if not image.flip_x:
                    coo[2] = -16, -16
                else:
                    coo[2] = 16, -16

            moment = pymunk.moment_for_poly(self.weight, coo)
            body = pymunk.Body(self.weight, moment)
            shape = pymunk.Poly(body, coo)
            self._set_body_shape(body, shape)

            temp = self.space_ship.sprites_creation[self.pos_ship[1]][self.pos_ship[0]][1].image
            img = self.space_ship.Var.image["triangular block"].get_transform(flip_x=temp.flip_x, flip_y=temp.flip_y)
            img.anchor_x = img.width // 2
            img.anchor_y = img.height // 2

            self.sprite = pyglet.sprite.Sprite(
                            img,
                            x=self.pos[0],
                            y=self.pos[1],
                            batch=self.space_ship.batch,
                            group=self.space_ship.z1
                            )

    def _init_(self):
        image = self.space_ship.sprites_creation[self.pos_ship[1]][self.pos_ship[0]][1].image
        top = False
        if image.flip_y:
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
        if not image.flip_y:
            if self.pos_ship[1] != 0:
                element_bottom = self.space_ship.sprites_creation[self.pos_ship[1] - 1][self.pos_ship[0]]
                if element_bottom[0]:
                    if not element_bottom[0] in ("triangular block", "reactor", "cannon", "torpedo launch"):
                        bottom = True
                    elif element_bottom[0] == "triangular block":
                        if element_bottom[1].image.flip_y:
                            bottom = True
                    elif element_bottom[0] == "reactor":
                        if not element_bottom[1].image.flip_y:
                            bottom = True
                    elif element_bottom[0] == "torpedo launch":
                        if element_bottom[1].image.flip_y:
                            bottom = True

        left = False
        if not image.flip_x:
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
        if image.flip_x:
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

    def help_info(self, consumption_label, label1, response_label1, label2, response_label2):
        consumption_label.text = "0"
        label1.text = ""
        response_label1.text = ""
        label2.text = ""
        response_label2.text = ""
