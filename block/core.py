#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  core.py
#
#  Copyright 2019 Nicolas Pengov <nicolas.pengov@sfr.fr>
#


#   ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~   IMPORT
import pymunkoptions
pymunkoptions.options["debug"] = False
import pymunk
from .model_block import ModelBlock
import pyglet
from random import randrange


#   ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~   CLASS
class Core(ModelBlock):

    def __init__(self, pos_ship, space_ship, nothing=False):
        super(Core, self).__init__(
                life=1000,
                weight=1500,
                space_ship=space_ship,
                pos_ship=pos_ship,
                COST=0
                )

        if not nothing:
            moment = pymunk.moment_for_box(self.weight, (32, 32))
            body = pymunk.Body(self.weight, moment)
            body.position = 500, 500
            shape = pymunk.Poly(body, [(-16, -16), (-16, 16), (16, 16), (16, -16)])
            self._set_body_shape(body, shape)

            temp = self.space_ship.sprites_creation[self.pos_ship[1]][self.pos_ship[0]][1].image
            if self.space_ship == self.space_ship.Var.main_space_ship:
                img = self.space_ship.Var.image["core"].get_transform(flip_x=temp.flip_x, flip_y=temp.flip_y)
            else:
                img = self.space_ship.Var.image["core evil"].get_transform(flip_x=temp.flip_x, flip_y=temp.flip_y)
            img.anchor_x = img.width // 2
            img.anchor_y = img.height // 2

            self.sprite = pyglet.sprite.Sprite(
                            img,
                            x=self.pos[0],
                            y=self.pos[1],
                            batch=self.space_ship.batch,
                            group=self.space_ship.z0
                            )

            self.space_ship.pos_core = pos_ship

    def delete(self, anim=False):
        super(Core, self).delete()
        if not anim:
            for line in self.space_ship.objects:
                for element in line:
                    if element:
                        element.delete()
        else:
            for line in self.space_ship.objects:
                for element in line:
                    if element not in (None, self):
                        if element.joint_side["top"]:
                            element.space_ship.Var.space.remove(element.joint_side["top"])
                            element.space_ship.objects[element.pos_ship[1]][element.pos_ship[0]].joint_side["top"] = False
                        if element.joint_side["bottom"]:
                            element.space_ship.Var.space.remove(element.joint_side["bottom"])
                            element.space_ship.objects[element.pos_ship[1]][element.pos_ship[0]].joint_side["bottom"] = False
                        if element.joint_side["right"]:
                            element.space_ship.Var.space.remove(element.joint_side["right"])
                            element.space_ship.objects[element.pos_ship[1]][element.pos_ship[0]].joint_side["right"] = False
                        if element.joint_side["left"]:
                            element.space_ship.Var.space.remove(element.joint_side["left"])
                            element.space_ship.objects[element.pos_ship[1]][element.pos_ship[0]].joint_side["left"] = False

                        element.body.apply_impulse_at_local_point(
                                (randrange(-500_000, 500_000), randrange(-500_000, 500_000)),
                                (randrange(-16, 16), randrange(-16, 16)))

    def help_info(self, consumption_label, label1, response_label1, label2, response_label2):
        consumption_label.text = "0"
        label1.text = ""
        response_label1.text = ""
        label2.text = ""
        response_label2.text = ""
