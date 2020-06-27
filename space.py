#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  space.py
#
#  Copyright 2019 Nicolas Pengov <nicolas.pengov@sfr.fr>
#


#   ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~   IMPORT
import pymunkoptions
pymunkoptions.options["debug"] = False
import pymunk
from bot import Bot


#   ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~   CLASS
class Space(pymunk.Space):
    def __init__(self, Var):
        super(Space, self).__init__()
        self.Var = Var
        self.gravity = 0, 0

        self.game = None
        self.border = []

        self.ship = []
        self.bot = []

    def set_game(self, game):
        self.remove(*self.border)
        self.border = []

        self.border.append(pymunk.Segment(
                                                            self.Var.space.static_body,
                                                            (-10, self.Var.SCREEN_SIZE[1] + 10),
                                                            (self.Var.SCREEN_SIZE[0] + 10, self.Var.SCREEN_SIZE[1] + 10),
                                                            10))
        self.border[-1].position = 0, 0
        self.border[-1].elasticity = 0.0
        self.border[-1].friction = .75
        self.border.append(pymunk.Segment(self.Var.space.static_body, (-10, -10), (-10, self.Var.SCREEN_SIZE[1] + 10), 10))
        self.border[-1].position = 0, 0
        self.border[-1].elasticity = 0.0
        self.border[-1].friction = .75
        self.border.append(pymunk.Segment(self.Var.space.static_body, (-10, -10), (self.Var.SCREEN_SIZE[0] + 10, -10), 10))
        self.border[-1].position = 0, 0
        self.border[-1].elasticity = 0.0
        self.border[-1].friction = .75
        self.border.append(pymunk.Segment(
                                                            self.Var.space.static_body,
                                                            (self.Var.SCREEN_SIZE[0] + 10, -10),
                                                            (self.Var.SCREEN_SIZE[0] + 10, self.Var.SCREEN_SIZE[1] + 10),
                                                            10))
        self.border[-1].position = 0, 0
        self.border[-1].elasticity = 0.0
        self.border[-1].friction = .75

        try:
            self.add(*self.border)
        except AssertionError:
            pass

        self.game = game

    def add_ship(self, ship) -> int:
        if ship != self.Var.main_space_ship and self.Var.current_scene == "player vs bot":
            ship.bot = Bot(ship)
            self.bot.append(ship)
        self.ship.append(ship)
        id = len(self.ship)

        h = self.add_collision_handler(id, id + 100)

        def begin(arbiter, space, data):
            for ship in self.ship:
                for bullet in ship.bullet:
                    if bullet.shape == arbiter.shapes[1]:
                        if bullet.attack_own_ship:
                            for line in ship.objects:
                                for object_ in line:
                                    if object_:
                                        if arbiter.shapes[0] == object_.shape:
                                            object_.life -= bullet.damage * bullet.bonus_block
                                            if object_.life <= 0:
                                                if "core" in str(object_):
                                                    object_.delete(anim=True)
                                                    if self.Var.sfx:
                                                        self.Var.music["sfx"]["core explosion"].play()
                                                else:
                                                    object_.delete()
                                                    if self.Var.sfx:
                                                        self.Var.music["sfx"]["explosion"].play()
                                            else:
                                                if self.Var.sfx:
                                                    self.Var.music["sfx"]["block hit"].play()
                                            object_.detect_critique()
                            bullet.delete()
                            return True
                        else:
                            return False
            else:
                return True
        h.begin = begin

        h = self.add_wildcard_collision_handler(id + 100)

        def begin(arbiter, space, data):
            for ship in self.ship:
                for bullet in ship.bullet:
                    if bullet.shape == arbiter.shapes[0]:
                        if 0 < arbiter.shapes[1].collision_type < 100:
                            for ship in self.ship:
                                for line in ship.objects:
                                    for object_ in line:
                                        if object_:
                                            if arbiter.shapes[1] == object_.shape:
                                                object_.life -= bullet.damage * bullet.bonus_block
                                                if object_.life <= 0:
                                                    if self.Var.current_scene != "multiplayer":
                                                        if "core" in str(object_):
                                                            object_.delete(anim=True)
                                                            if self.Var.sfx:
                                                                self.Var.music["sfx"]["core explosion"].play()
                                                        else:
                                                            object_.delete()
                                                            if self.Var.sfx:
                                                                self.Var.music["sfx"]["explosion"].play()
                                                    else:
                                                        if object_.space_ship == self.Var.main_space_ship:
                                                            self.Var.client.send("DEL:" + str(object_.pos_ship[0]) + "|" +
                                                                                 str(object_.pos_ship[1]))
                                                            if "core" in str(object_):
                                                                object_.delete(anim=True)
                                                                if self.Var.sfx:
                                                                    self.Var.music["sfx"]["core explosion"].play()
                                                            else:
                                                                object_.delete()
                                                                if self.Var.sfx:
                                                                    self.Var.music["sfx"]["explosion"].play()
                                                else:
                                                    if self.Var.sfx:
                                                        self.Var.music["sfx"]["block hit"].play()
                        bullet.delete()
                        return True
            return True
        h.begin = begin

        return id
