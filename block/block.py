#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  block.py
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
class Block(ModelBlock):
    def __init__(self, pos_ship, space_ship, nothing=False):
        super(Block, self).__init__(
                life=1000,
                weight=1000,
                space_ship=space_ship,
                pos_ship=pos_ship,
                COST=20
                )

        if not nothing:
            moment = pymunk.moment_for_box(self.weight, (32, 32))
            body = pymunk.Body(self.weight, moment)
            shape = pymunk.Poly(body, [(-16, -16), (-16, 16), (16, 16), (16, -16)])
            self._set_body_shape(body, shape)

            temp = self.space_ship.sprites_creation[self.pos_ship[1]][self.pos_ship[0]][1].image
            img = self.space_ship.Var.image["block"].get_transform(flip_x=temp.flip_x, flip_y=temp.flip_y)
            img.anchor_x = img.width // 2
            img.anchor_y = img.height // 2

            self.sprite = pyglet.sprite.Sprite(
                            img,
                            x=self.pos[0],
                            y=self.pos[1],
                            batch=self.space_ship.batch,
                            group=self.space_ship.z0
                            )

    def help_info(self, consumption_label, label1, response_label1, label2, response_label2):
        consumption_label.text = "0"
        label1.text = ""
        response_label1.text = ""
        label2.text = ""
        response_label2.text = ""
