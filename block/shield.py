#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  shield.py
#
#  Copyright 2019 Nicolas Pengov <nicolas.pengov@sfr.fr>
#


#   ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~   IMPORT
import pymunkoptions
pymunkoptions.options["debug"] = False
import pymunk
from .model_block import ModelBlock
import pyglet
from math import sqrt


#   ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~   CLASS
class Shield(ModelBlock):
    def __init__(self, pos_ship, space_ship, nothing=False):
        super(Shield, self).__init__(
                life=750,
                weight=500,
                STORAGE_MAX=10,
                CRITICAL_LIFE=250,
                RECV_MAX=4,
                space_ship=space_ship,
                pos_ship=pos_ship,
                COST=100
                )

        self.RANGE_MAX = 20 * 16 // 2
        self.RANGE_MIN = 19 * 16 // 2

        self.SHIELD_LIFE_MAX = self.life * 10
        self.shield_life = self.SHIELD_LIFE_MAX // 2
        self.CONSUMPTION = 2
        self.REGEN_CONSUMPTION_MAX = 3
        self.LIFE_PER_ENERGY = 300

        self.breakdown_time = 0
        self.BREAKDOWN_TIME = 7.5
        self.breakdown_energy = 0
        self.BREAKDOWN_ENERGY = 20

        self.shield_animation_tick = 0

        if not nothing:
            moment = pymunk.moment_for_box(self.weight, (32, 32))
            body = pymunk.Body(self.weight, moment)
            shape = pymunk.Poly(body, [(-16, -16), (-16, 16), (16, 16), (16, -16)])
            self._set_body_shape(body, shape)

            temp = self.space_ship.sprites_creation[self.pos_ship[1]][self.pos_ship[0]][1].image
            if self.space_ship == self.space_ship.Var.main_space_ship:
                img = self.space_ship.Var.image["shield"].get_transform(flip_x=temp.flip_x, flip_y=temp.flip_y)
            else:
                img = self.space_ship.Var.image["shield evil"].get_transform(flip_x=temp.flip_x, flip_y=temp.flip_y)
            img.anchor_x = img.width // 2
            img.anchor_y = img.height // 2

            self.sprite = pyglet.sprite.Sprite(
                            img,
                            x=self.pos[0],
                            y=self.pos[1],
                            batch=self.space_ship.batch,
                            group=self.space_ship.z0
                            )

            if self.space_ship == self.space_ship.Var.main_space_ship:
                img = self.space_ship.Var.image["shield projection"].get_transform()
            else:
                img = self.space_ship.Var.image["shield projection evil"].get_transform()
            img.anchor_x = img.width // 2
            img.anchor_y = img.height // 2

            self.shield_sprite = pyglet.sprite.Sprite(
                            img,
                            x=self.pos[0],
                            y=self.pos[1],
                            batch=self.space_ship.batch,
                            group=self.space_ship.z2
                            )

    def set_pos(self, pos):
        super(Shield, self).set_pos(pos)
        self.shield_sprite.x, self.shield_sprite.y = pos

    def update_pos(self):
        super(Shield, self).update_pos()
        self.shield_sprite.x, self.shield_sprite.y = self.body.position

    def update(self, dt):
        if self.shield_life > 0:
            if self.shield_life < self.SHIELD_LIFE_MAX * 2 / 15:
                if self.shield_animation_tick >= 0.1:
                    self.shield_sprite.visible = not self.shield_sprite.visible
                    self.shield_animation_tick = 0
                else:
                    self.shield_animation_tick += dt
            else:
                self.shield_sprite.visible = True

            if self.storage >= self.CONSUMPTION * dt:
                self.storage -= self.CONSUMPTION * dt
            else:
                self.shield_life = max(0, self.shield_life - self.SHIELD_LIFE_MAX * 0.1 * dt)

            if self.storage:
                energy_use = min(
                                                self.storage, self.REGEN_CONSUMPTION_MAX * dt,
                                                (self.SHIELD_LIFE_MAX - self.shield_life) / self.LIFE_PER_ENERGY)
                self.storage -= energy_use
                self.shield_life += energy_use * self.LIFE_PER_ENERGY

            for ship in self.space_ship.Var.space.ship:
                if ship is not self.space_ship:
                    for bullet in ship.bullet:
                        pos_bullet = bullet.body.position
                        distance = sqrt((pos_bullet[0] - self.pos[0]) ** 2 + (pos_bullet[1] - self.pos[1]) ** 2)
                        if distance <= self.RANGE_MAX:
                            last_pos_bullet = pos_bullet - bullet.body.velocity * dt
                            last_distance = sqrt(
                                                (last_pos_bullet[0] - self.pos[0]) ** 2 +
                                                (last_pos_bullet[1] - self.pos[1]) ** 2)
                            if last_distance >= self.RANGE_MIN:
                                self.shield_life = max(0, self.shield_life - bullet.damage * bullet.bonus_shield)
                                bullet.delete()
                                if self.space_ship.Var.sfx:
                                    self.space_ship.Var.music["sfx"]["shield hit"].play()
        else:
            if self.shield_sprite.visible:
                if self.space_ship.Var.sfx:
                    self.space_ship.Var.music["sfx"]["dead shield"].play()
                self.shield_sprite.visible = False
            energy = min(self.storage, self.BREAKDOWN_ENERGY - self.breakdown_energy)
            self.breakdown_energy += energy
            self.storage -= energy
            self.breakdown_time += dt
            if self.breakdown_time >= self.BREAKDOWN_TIME and self.breakdown_energy >= self.BREAKDOWN_ENERGY:
                self.BREAKDOWN_TIME += 0.5
                self.breakdown_time = 0
                self.breakdown_energy = 0
                self.shield_life = self.SHIELD_LIFE_MAX // 3

    def detect_critique(self):
        if super(Shield, self).detect_critique():
            self.SHIELD_LIFE_MAX *= 2/3
            self.LIFE_PER_ENERGY = 200
            self.breakdown_time + 1.5

    def help_info(self, consumption_label, label1, response_label1, label2, response_label2):
        consumption_label.text = "passif: " + str(self.CONSUMPTION) + "/s\nactif: " + str(self.REGEN_CONSUMPTION_MAX) + "/s)"
        label1.text = "Radius:"
        response_label1.text = str(self.RANGE_MAX // 32 - 1) + " block"
        label2.text = "Shield Life:"
        response_label2.text = str(self.SHIELD_LIFE_MAX)
