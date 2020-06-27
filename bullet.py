#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  bullet.py
#
#  Copyright 2019 Nicolas Pengov <nicolas.pengov@sfr.fr>
#


#   ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~   IMPORT
import pymunkoptions
pymunkoptions.options["debug"] = False
import pymunk
import pyglet
import random
from math import pi, acos
random.seed(25566)


#   ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~   CLASS
class Bullet:
    """
    Parent class to the different bullet class
    represents a shot in the game: turret, cannon, torpedo launch
    """
    def __init__(self, angle, pos, space_ship):
        self.space_ship = space_ship
        self.pos = pos
        self.angle = angle

        self.THRUST = 100_000
        self.damage = 10
        self.weight = 120

        #   a damage bonus for the blocks or the shields
        self.bonus_block = 1
        self.bonus_shield = 1

        #   can attack her own ship, only False for TurretBullet
        self.attack_own_ship = True

        img = self.space_ship.Var.image["bullet"].get_transform()
        img.anchor_x = img.width // 2
        img.anchor_y = img.height // 2
        self.sprite = pyglet.sprite.Sprite(
                        img,
                        x=self.pos[0],
                        y=self.pos[1],
                        batch=self.space_ship.batch,
                        group=self.space_ship.z0
                        )

        self.body = None
        self.shape = None

        self.space_ship.bullet.append(self)

    def _init_(self):
        """init phycally and give a speed on the bullet"""

        moment = pymunk.moment_for_box(self.weight, (8, 8))
        self.body = pymunk.Body(self.weight, moment)
        self.shape = pymunk.Poly(self.body, [(-4, -4), (-4, 4), (4, 4), (4, -4)])
        self.space_ship.Var.space.add(self.body, self.shape)

        self.body.position = self.pos
        self.body.angle = self.angle
        self.shape.collision_type = self.space_ship.id + 100

        self.body.apply_impulse_at_local_point((0, self.THRUST), (0, 0))

    def update_pos(self):
        """call in the game loop
        update the new position of the bullet"""

        if self.body:
            self.pos = self.body.position
            self.sprite.x, self.sprite.y = self.body.position
        else:
            self.sprite.x, self.sprite.y = self.pos

    def set_pos(self, pos):
        self.pos = pos
        self.body.position = pos
        self.sprite.x, self.sprite.y = pos

    def get_pos(self):
        return pymunk.Vec2d(self.pos)

    def delete(self):
        """delete the bullet of the world, graphically, physically, computationally"""
        for i in range(len(self.space_ship.bullet)):
            if self.space_ship.bullet[i] == self:
                del self.space_ship.bullet[i]
                break
        self.space_ship.Var.space.remove(self.body, self.shape)
        del self.sprite


class CannonBullet(Bullet):
    DAMAGE = 100

    def __init__(self, angle, pos, space_ship):
        super(CannonBullet, self).__init__(angle, pos, space_ship)
        self.damage = CannonBullet.DAMAGE
        self.bonus_block = 1.25
        self._init_()


class TurretBullet(Bullet):
    DAMAGE = 100

    def __init__(self, angle, pos, space_ship):
        angle += (random.random() * pi / 12) - pi / 24
        super(TurretBullet, self).__init__(angle, pos, space_ship)
        self.attack_own_ship = False
        self.damage = TurretBullet.DAMAGE
        self.THRUST = 85_000
        self._init_()


class TorpedoBullet(Bullet):
    DAMAGE = 500

    def __init__(self, angle, pos, space_ship, pos_click, evil):
        super(TorpedoBullet, self).__init__(angle, pos, space_ship)
        self.damage = TorpedoBullet.DAMAGE
        self.THRUST = 250_000
        self.weight = 750
        self.bonus_shield = 1.25
        self.life = 5

        self.pos_click = pos_click

        if not evil:
            img = self.space_ship.Var.image["torpedo bullet"].get_transform()
        else:
            img = self.space_ship.Var.image["torpedo bullet evil"].get_transform()
        img.anchor_x = img.width // 2
        img.anchor_y = img.height // 2
        self.sprite = pyglet.sprite.Sprite(
                        img,
                        x=self.pos[0],
                        y=self.pos[1],
                        batch=self.space_ship.batch,
                        group=self.space_ship.z0
                        )

        self._init_()

    def _init_(self):
        self.sprite.visible = True
        radius = 10
        moment = pymunk.moment_for_circle(self.weight, 0, radius)
        self.body = pymunk.Body(self.weight, moment)
        self.shape = pymunk.Circle(self.body, radius)
        self.space_ship.Var.space.add(self.body, self.shape)

        self.body.position = self.pos
        self.body.angle = self.angle
        self.shape.collision_type = self.space_ship.id + 100

        self.body.apply_impulse_at_local_point((0, self.THRUST * 2 // 3), (0, 0))

    def update(self, dt):
        """TorpedoBullet is a special bullet
        he needs to have a update function to give a force to change the path"""

        pos = self.get_pos()
        delta = self.pos_click[0] - pos[0], self.pos_click[1] - pos[1]
        angle = acos((delta[0]) / (delta[0] ** 2 + delta[1] ** 2) ** 0.5) - pi/2
        if delta[1] < 0:
            angle *= -1
            angle += pi
        self.body.angle = angle

        self.body.apply_force_at_local_point((0, self.THRUST), (0, 0))
        self.THRUST *= (1 + dt / 3)
        self.life -= dt
        if self.life <= 0:
            self.delete()
