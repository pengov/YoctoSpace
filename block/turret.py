#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  turret.py
#
#  Copyright 2019 Nicolas Pengov <nicolas.pengov@sfr.fr>
#


#   ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~   IMPORT
import pymunkoptions
pymunkoptions.options["debug"] = False
import pymunk
from .model_block import ModelBlock
import pyglet
from math import pi, acos, cos, sin
from bullet import TurretBullet


#   ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~   CLASS
class Turret(ModelBlock):
    def __init__(self, pos_ship, space_ship, nothing=False):
        super(Turret, self).__init__(
                life=750,
                weight=1500,
                STORAGE_MAX=5,
                RECV_MAX=3,
                space_ship=space_ship,
                pos_ship=pos_ship,
                COST=50
                )

        self._shot = False
        self.shot_pos = None
        self.ANGLE_MAX_CORRECTION = 90
        self.RELOADING = 1
        self.reloading = 0
        self.ENERGY_PER_SHOT = 0.75
        self.ENERGY_PER_TOUR = 4

        if not nothing:
            moment = pymunk.moment_for_box(self.weight, (32, 32))
            body = pymunk.Body(self.weight, moment)
            shape = pymunk.Poly(body, [(-16, -16), (-16, 16), (16, 16), (16, -16)])
            self._set_body_shape(body, shape)

            temp = self.space_ship.sprites_creation[self.pos_ship[1]][self.pos_ship[0]][1].image
            img = self.space_ship.Var.image["base turret"].get_transform(flip_x=temp.flip_x, flip_y=temp.flip_y)
            img.anchor_x = img.width // 2
            img.anchor_y = img.height // 2

            self.sprite = pyglet.sprite.Sprite(
                            img,
                            x=self.pos[0],
                            y=self.pos[1],
                            batch=self.space_ship.batch,
                            group=self.space_ship.z0
                            )

            temp = self.space_ship.sprites_creation[self.pos_ship[1]][self.pos_ship[0]][1].image
            img = self.space_ship.Var.image["weapon turret"].get_transform(flip_x=temp.flip_x, flip_y=temp.flip_y)
            img.anchor_x = img.width // 2
            img.anchor_y = img.height // 3

            self.weapon_sprite = pyglet.sprite.Sprite(
                            img,
                            x=self.pos[0],
                            y=self.pos[1],
                            batch=self.space_ship.batch,
                            group=self.space_ship.z1
                            )

    def init_pos(self, space_ship_pos, side, len_width, len_height):
        super(Turret, self).init_pos(space_ship_pos, side, len_width, len_height)
        self.weapon_sprite.rotation = self.sprite.rotation

    def set_pos(self, pos):
        super(Turret, self).set_pos(pos)
        self.weapon_sprite.x, self.sprite.y = pos

    def update_pos(self):
        super(Turret, self).update_pos()
        self.weapon_sprite.x, self.weapon_sprite.y = self.body.position

    def shot(self, shot_pos=None):
        self._shot = True
        self.shot_pos = shot_pos

    def stop_shot(self):
        self._shot = False
        self.shot_pos = None

    def update(self, dt):
        self.reloading += dt
        if self._shot:
            if self.space_ship.Var.current_scene != "multiplayer" or self.space_ship == self.space_ship.Var.main_space_ship:
                shot_pos = self.space_ship.Var.mouse_position if not self.shot_pos else self.shot_pos
            else:
                shot_pos = self.space_ship.shot_pos
            pos = self.get_pos()
            delta = shot_pos[0] - pos[0], shot_pos[1] - pos[1]
            angle = acos(delta[0] / (delta[0] ** 2 + delta[1] ** 2) ** 0.5)
            angle *= -1 if shot_pos[1] - pos[1] < 0 else 1

            angle_degree = -angle * 180 / pi + 90
            angle_degree = 360 + angle_degree if angle_degree < 0 else angle_degree

            delta_angle = angle_degree - self.weapon_sprite.rotation
            if abs(delta_angle) > 180:
                delta_angle *= -1
                delta_angle += -180 if delta_angle > 0 else 180

            if delta_angle != 0:
                corection = min(abs(delta_angle), self.ANGLE_MAX_CORRECTION * dt) * delta_angle / abs(delta_angle)
                if self.storage >= self.ENERGY_PER_TOUR * abs(corection / 360):
                    self.storage -= self.ENERGY_PER_TOUR * abs(corection / 360)
                    self.weapon_sprite.rotation = self.weapon_sprite.rotation % 360 + corection

            if self.weapon_sprite.rotation == angle_degree:
                if self.reloading >= self.RELOADING:
                    if self.storage >= self.ENERGY_PER_SHOT:
                        self.storage -= self.ENERGY_PER_SHOT
                        self.reloading = 0
                        angle -= pi / 2
                        pos = pos[0] + sin(-angle) * 16, pos[1] + cos(-angle) * 16
                        if self.space_ship.Var.sfx:
                            self.space_ship.Var.music["sfx"]["turret shot"].play()
                        TurretBullet(angle, pos, self.space_ship)

    def help_info(self, consumption_label, label1, response_label1, label2, response_label2):
        consumption_label.text = str(self.ENERGY_PER_SHOT) + "/shot"
        label1.text = "Reload:"
        response_label1.text = str(self.RELOADING) + "s"
        label2.text = "Damage:"
        response_label2.text = str(TurretBullet.DAMAGE)
