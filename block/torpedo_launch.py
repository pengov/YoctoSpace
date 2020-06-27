#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  torpedo_launch.py
#
#  Copyright 2019 Nicolas Pengov <nicolas.pengov@sfr.fr>
#


#   ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~   IMPORT
import pymunkoptions
pymunkoptions.options["debug"] = False
import pymunk
from .model_block import ModelBlock
import pyglet
from math import pi, sin, cos
from bullet import TorpedoBullet


#   ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~   CLASS
class TorpedoLaunch(ModelBlock):
    def __init__(self, pos_ship, space_ship, nothing=False):
        super(TorpedoLaunch, self).__init__(
                life=250,
                weight=1500,
                STORAGE_MAX=10,
                RECV_MAX=3,
                space_ship=space_ship,
                pos_ship=pos_ship,
                COST=80
                )

        self.RELOADING = 2
        self.reloading = 0
        self.ENERGY_PER_SHOT = 2
        self.ENERGY_RELOAD = 4
        self.evil = False

        if not nothing:
            temp = self.space_ship.sprites_creation[self.pos_ship[1]][self.pos_ship[0]][1].image

            coo = [
                        (-14, -16), (-14, -5), (-9, -5), (-9, 8), (-6, 8),
                        (-6, -4), (6, 4), (6, 8), (9, 8), (9, -5), (14, -5), (14, -16)
                        ]
            if temp.flip_y:
                for i, element in enumerate(coo):
                    coo[i] = element[0], -element[1]

            moment = pymunk.moment_for_poly(self.weight, coo)
            body = pymunk.Body(self.weight, moment)
            shape = pymunk.Poly(body, coo)
            self._set_body_shape(body, shape)

            self.img = self.space_ship.Var.image["torpedo launch"].get_transform(flip_x=temp.flip_x, flip_y=temp.flip_y)
            self.img.anchor_x = self.img.width // 2
            self.img.anchor_y = self.img.height // 3 * 2

            self.sprite = pyglet.sprite.Sprite(
                            self.img,
                            x=self.pos[0],
                            y=self.pos[1],
                            batch=self.space_ship.batch,
                            group=self.space_ship.z0
                            )

            if self.space_ship == self.space_ship.Var.main_space_ship:
                self.img_load = self.space_ship.Var.image["torpedo launch load"].get_transform(
                                                    flip_x=temp.flip_x,
                                                    flip_y=temp.flip_y)
                self.evil = False
            else:
                self.img_load = self.space_ship.Var.image["torpedo launch load evil"].get_transform(
                                                    flip_x=temp.flip_x,
                                                    flip_y=temp.flip_y)
                self.evil = True
            self.img_load.anchor_x = self.img_load.width // 2
            self.img_load.anchor_y = self.img_load.height // 3 * 2

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
        right = False

        self._set_joint_side(top, bottom, left, right)

    def shot(self, pos_click):
        if self.storage >= self.ENERGY_PER_SHOT and self.reloading >= self.RELOADING:
            self.storage -= self.ENERGY_PER_SHOT
            self.reloading = 0

            flip_y = self.space_ship.sprites_creation[self.pos_ship[1]][self.pos_ship[0]][1].image.flip_y
            angle = self.body.angle + pi if flip_y else self.body.angle
            pos = self.get_pos()
            pos = pos[0] + sin(-angle) * 32, pos[1] + cos(-angle) * 32
            if self.space_ship.Var.current_scene == "multiplayer" and self.space_ship is not self.space_ship.Var.main_space_ship:
                if self.space_ship.Var.to_do != "":
                    self.space_ship.Var.to_do += "torpedo bullet", angle, pos, self.space_ship, pos_click, self.evil
                else:
                    self.space_ship.Var.to_do = "torpedo bullet", angle, pos, self.space_ship, pos_click, self.evil
            else:
                TorpedoBullet(angle, pos, self.space_ship, pos_click, self.evil)
            if self.space_ship.Var.sfx:
                self.space_ship.Var.music["sfx"]["torpedo shot"].play()
            self.sprite.image = self.img

    def update(self, dt):
        if self.storage and self.reloading < self.RELOADING:
            energy = min(
                                    self.storage, self.ENERGY_RELOAD / self.RELOADING * dt,
                                    (self.RELOADING - self.reloading) * self.ENERGY_RELOAD)
            self.storage -= energy
            self.reloading += energy / self.ENERGY_RELOAD * self.RELOADING

        elif self.storage >= self.ENERGY_PER_SHOT and self.reloading >= self.RELOADING:
            self.sprite.image = self.img_load

    def help_info(self, consumption_label, label1, response_label1, label2, response_label2):
        consumption_label.text = str(self.ENERGY_RELOAD) + "/reload" + "\n" + str(self.ENERGY_PER_SHOT) + "/shot"
        label1.text = "Reload:"
        response_label1.text = str(self.RELOADING) + "s"
        label2.text = "Damage:"
        response_label2.text = str(TorpedoBullet.DAMAGE)
