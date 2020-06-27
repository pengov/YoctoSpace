#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  space_ship.py
#
#  Copyright 2019 Nicolas Pengov <nicolas.pengov@sfr.fr>
#


#   ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~   IMPORT
import pymunkoptions
pymunkoptions.options["debug"] = False
import pymunk
from pymunk import Vec2d
import pyglet
import block
import pickle
from os.path import abspath
from time import sleep
from math import radians, sin
from random import randint


#   ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~   CLASS
class SpaceShip:
    #   a ship has a maximum size of 13*13
    SIZE_MAX = 13, 13
    Var = None

    def __init__(self, Var=None):
        """
        SpaceShip class initialization function
        """

        if not SpaceShip.Var and Var:
            SpaceShip.Var = Var
            if Var.main_space_ship is None:
                Var.main_space_ship = self

        self.bot = None
        self.id = self.Var.space.add_ship(self)

        #   position of the ship's core
        #   if this one is destroyed, the whole ship explodes
        self.pos_core = (0, 0)

        self.batch = pyglet.graphics.Batch()
        self.objects = []
        #   the coordinates start at the bottom right
        for i in range(self.SIZE_MAX[0]):
            self.objects.append([])
            for i in range(self.SIZE_MAX[1]):
                self.objects[-1].append(None)

        self.batch_creation = pyglet.graphics.Batch()
        self.sprites_creation = []
        #   it's a copy of sprites_creation but he not will cut
        self.sprites_creation_copy = []
        #   the coordinates start at the bottom right
        for i in range(self.SIZE_MAX[0]):
            self.sprites_creation.append([])
            self.sprites_creation_copy.append([])
            for i in range(self.SIZE_MAX[1]):
                self.sprites_creation[-1].append((None, None))
                self.sprites_creation_copy[-1].append((None, None))

        #   the different sprites display priority layers
        self.z0 = pyglet.graphics.OrderedGroup(0)
        self.z1 = pyglet.graphics.OrderedGroup(1)
        self.z2 = pyglet.graphics.OrderedGroup(2)

        #   contain all classic bullet shoting from the ship
        self.bullet = []
        #   contain the torpedo bullet shoting from the ship
        self.torpedo_bullet = []

        #   for multiplayer
        self.last_reactor_x = 0
        self.last_reactor_y = 0

    def _create_ship(self) -> None:
        """
        Function to be used only once for its initialization
        Already used in the initialization of it
        Allows to create for each element of the ship the corresponding object
        """

        for i, line in enumerate(self.sprites_creation):
            for j, element in enumerate(line):
                if element[0] is None:
                    continue
                elif element[0] == "core":
                    self.objects[i][j] = block.Core((j, i), self)
                    self.objects[i][j]._init_()
                elif element[0] == "block":
                    self.objects[i][j] = block.Block((j, i), self)
                    self.objects[i][j]._init_()
                elif element[0] == "reinforced block":
                    self.objects[i][j] = block.ReinforcedBlock((j, i), self)
                    self.objects[i][j]._init_()
                elif element[0] == "triangular block":
                    self.objects[i][j] = block.TriangularBlock((j, i), self)
                    self.objects[i][j]._init_()
                elif element[0] == "generator":
                    self.objects[i][j] = block.Generator((j, i), self)
                    self.objects[i][j]._init_()
                elif element[0] == "battery":
                    self.objects[i][j] = block.Battery((j, i), self)
                    self.objects[i][j]._init_()
                elif element[0] == "shield":
                    self.objects[i][j] = block.Shield((j, i), self)
                    self.objects[i][j]._init_()
                elif element[0] == "reactor":
                    self.objects[i][j] = block.Reactor((j, i), self)
                    self.objects[i][j]._init_()
                elif element[0] == "cannon":
                    self.objects[i][j] = block.Cannon((j, i), self)
                    self.objects[i][j]._init_()
                elif element[0] == "turret":
                    self.objects[i][j] = block.Turret((j, i), self)
                    self.objects[i][j]._init_()
                elif element[0] == "torpedo launch":
                    self.objects[i][j] = block.TorpedoLaunch((j, i), self)
                    self.objects[i][j]._init_()
                else:
                    raise AttributeError(element[0])

        self._init_joint_element()
        self._init_pos_element()

    def _init_pos_element(self) -> None:
        """
        Function to be used only once for its initialization
        Already used in the initialization of it
        Allows to calculate for each object of the ship from its position
        """

        init_pos = self.Var.SCREEN_SIZE[0] / 2, self.Var.SCREEN_SIZE[1] / 2
        side = "left"
        if self.Var.mode == "training":
            side = "top"
        elif self.Var.mode == "player vs bot":
            if self == self.Var.main_space_ship:
                init_pos = self.Var.SCREEN_SIZE[0] // 5, self.Var.SCREEN_SIZE[1] // 2
            else:
                init_pos = self.Var.SCREEN_SIZE[0] * 4 // 5, self.Var.SCREEN_SIZE[1] // 2
                side = "right"
        elif self.Var.mode == "multiplayer":
            #   wait the information "is_left_player"
            sleep(0.1)
            if self.Var.client.is_left_player:
                if self == self.Var.main_space_ship:
                    init_pos = self.Var.SCREEN_SIZE[0] // 5, self.Var.SCREEN_SIZE[1] // 2
                else:
                    init_pos = self.Var.SCREEN_SIZE[0] * 4 // 5, self.Var.SCREEN_SIZE[1] // 2
                    side = "right"
            else:
                if self == self.Var.main_space_ship:
                    init_pos = self.Var.SCREEN_SIZE[0] * 4 // 5, self.Var.SCREEN_SIZE[1] // 2
                    side = "right"
                else:
                    init_pos = self.Var.SCREEN_SIZE[0] // 5, self.Var.SCREEN_SIZE[1] // 2

        for line in self.objects:
            for element in line:
                if element:
                    element.init_pos(init_pos, side, len(self.objects) - 1, len(self.objects[0]) - 1)

    def _init_joint_element(self) -> None:
        """
        Function to be used only once for its initialization
        Already used in the initialization of it
        Allows to create for each object of the ship its joints with the objects in the surroundings
        """

        for i, line in enumerate(self.objects):
            for j, element in enumerate(line):
                if element:
                    if element.joint_side["top"]:
                        joint = pymunk.PivotJoint(element.body, self.objects[i + 1][j].body, (0, 16), (0, -16))
                        element.joint_side["top"] = joint
                        self.Var.space.add(joint)
                    if element.joint_side["left"]:
                        joint = pymunk.PivotJoint(element.body, self.objects[i][j - 1].body, (-16, 0), (16, 0))
                        element.joint_side["left"] = joint
                        self.Var.space.add(joint)
                    if element.joint_side["bottom"]:
                        joint = pymunk.PivotJoint(element.body, self.objects[i - 1][j].body, (0, -16), (0, 16))
                        element.joint_side["bottom"] = joint
                        self.Var.space.add(joint)
                    if element.joint_side["right"]:
                        joint = pymunk.PivotJoint(element.body, self.objects[i][j + 1].body, (16, 0), (-16, 0))
                        element.joint_side["right"] = joint
                        self.Var.space.add(joint)

    def add_element(self, element: str, cell_x: int, cell_y: int) -> None:
        """
        Function allowing to add an element to the ship when creating it
        """

        self.del_element(cell_x, cell_y)
        if not element:
            return

        img = self.Var.image[element].get_transform(flip_x=self.Var.flip_x, flip_y=self.Var.flip_y)

        img.width *= 1.5
        img.height *= 1.5
        img.anchor_x = 0
        img.anchor_y = 0
        img.flip_x = self.Var.flip_x
        img.flip_y = self.Var.flip_y

        if element == "core":
            for i, line in enumerate(self.sprites_creation_copy):
                for j, column in enumerate(line):
                    if column[0] == "core":
                        self.del_element(j, i)
                        break

        elif element == "turret":
            img.anchor_x = img.width / 16 - 1
            img.anchor_y = img.height / 16 - 1

        elif element == "torpedo launch":
            if img.flip_y:
                img.anchor_y = img.height - img.height * 4 / 3

        elif element == "cannon":
            if img.flip_y:
                img.anchor_y = img.height // 2
                if cell_y != 0:
                    if self.sprites_creation_copy[cell_y - 1][cell_x][0]:
                        self.del_element(cell_x, cell_y - 1)
            else:
                if cell_y != self.SIZE_MAX[0] - 1:
                    if self.sprites_creation_copy[cell_y + 1][cell_x][0]:
                        self.del_element(cell_x, cell_y + 1)

        if cell_y != self.SIZE_MAX[0] - 1:
            if self.sprites_creation_copy[cell_y + 1][cell_x][0] == "cannon":
                if self.sprites_creation_copy[cell_y + 1][cell_x][1].image.flip_y:
                    self.del_element(cell_x, cell_y + 1)
        if cell_y != 0:
            if self.sprites_creation_copy[cell_y - 1][cell_x][0] == "cannon":
                if not self.sprites_creation_copy[cell_y - 1][cell_x][1].image.flip_y:
                    self.del_element(cell_x, cell_y - 1)

        sprite = pyglet.sprite.Sprite(
                        img,
                        x=48 * cell_x + self.Var.SCREEN_SIZE[0] // 2 - 32,
                        y=48 * cell_y + self.Var.SCREEN_SIZE[1] // 15,
                        batch=self.batch_creation
                        )

        if self.Var.main_space_ship is self:
            object_ = getattr(block, element.title().replace(" ", ""))((0, 0), self, nothing=True)
            self.Var.money -= object_.COST
            if self.Var.money >= 0:
                self.Var.scenes["creation"][1]["label"]["money"].color = 0, 255, 0, 255
            else:
                self.Var.scenes["creation"][1]["label"]["money"].color = 255, 0, 0, 255
            self.Var.scenes["creation"][1]["label"]["money"].text = "money: " + str(self.Var.money)

        self.sprites_creation_copy[cell_y][cell_x] = element, sprite

    def del_element(self, cell_x: int, cell_y: int) -> None:
        """
        Function allowing when creating the ship to delete an element from it
        """

        if self.sprites_creation_copy[cell_y][cell_x][0]:
            object_ = getattr(
                                      block,
                                      self.sprites_creation_copy[cell_y][cell_x][0].title().replace(" ", ""))(
                                            (0, 0),
                                            self,
                                            nothing=True)
            self.Var.money += object_.COST
            if self.Var.money >= 0:
                self.Var.scenes["creation"][1]["label"]["money"].color = 0, 255, 0, 255
            else:
                self.Var.scenes["creation"][1]["label"]["money"].color = 255, 0, 0, 255
            self.Var.scenes["creation"][1]["label"]["money"].text = "money: " + str(self.Var.money)
        self.sprites_creation_copy[cell_y][cell_x] = None, None

    def init(self) -> bool:
        """
        Function initializing the creation of the ship after the editing mode of the ship
        Called only once after the end of the ship's edition
        """

        #   Checks whether the ship complies with the constraints
        #   Which for the time being is limited to the presence of the ship's core
        #   Reset also sprites_creation and objects
        self.delete()
        self.sprites_creation = []
        self.objects = []
        for i, line in enumerate(self.sprites_creation_copy):
            self.sprites_creation.append([])
            self.objects.append([])
            for j, element in enumerate(line):
                self.sprites_creation[-1].append(element)
                self.objects[-1].append(None)

        if self.Var.money < 0 and self == self.Var.main_space_ship:
            return False

        correct_ship = False
        for line in self.sprites_creation:
            for element in line:
                if element[0] == "core":
                    correct_ship = True
                    break
        if not correct_ship:
            return correct_ship

        #   reduces the size of the matrix containing the information
        #   to a rectangular matrix containing all the information of the ship
        line_to_del = []
        for line in range(self.SIZE_MAX[1]):
            if self.sprites_creation[line].count((None, None)) == self.SIZE_MAX[0]:
                line_to_del.append(line)
            else:
                break

        for line in range(self.SIZE_MAX[1] - 1, -1, -1):
            if self.sprites_creation[line].count((None, None)) == self.SIZE_MAX[0]:
                line_to_del.append(line)
            else:
                break

        line_to_del.sort(reverse=True)

        for line in line_to_del:
            del self.objects[line]
            del self.sprites_creation[line]

        column_to_del = []
        for column in range(self.SIZE_MAX[0]):
            to_del = True
            for line in range(len(self.sprites_creation)):
                if self.sprites_creation[line][column] != (None, None):
                    to_del = False
                    break
            if to_del:
                column_to_del.append(column)
            else:
                break

        for column in range(self.SIZE_MAX[0] - 1, -1, -1):
            to_del = True
            for line in range(len(self.sprites_creation)):
                if self.sprites_creation[line][column] != (None, None):
                    to_del = False
                    break
            if to_del:
                column_to_del.append(column)
            else:
                break

        column_to_del.sort(reverse=True)

        for column in column_to_del:
            for line in range(len(self.objects)):
                del self.objects[line][column]
                del self.sprites_creation[line][column]

        #   create the objects for each element in the ship
        self._create_ship()

        return correct_ship

    @classmethod
    def create_bot(cls, nb_of_bot: int) -> tuple:
        if not cls.Var:
            raise Exception("Var is not defined.\ncreate a player space ship and give him the Var argument")

        space_ships = []
        for i in range(nb_of_bot):
            space_ship = SpaceShip()
            rand = str(randint(0, 3))
            space_ship.load("bot" + rand, bot=True)
            space_ships.append(space_ship)

        return tuple(space_ships)

    def update(self, dt: float) -> None:
        """
        function updating all the elements of the ship
        """

        for line in self.objects:
            for element in line:
                if element:
                    element.update_pos()
                    element.update_rotation()

                    if element.__class__ is block.Generator or\
                            element.__class__ is block.Battery:
                        element.update(dt, self.objects[:])

                    elif element.__class__ is block.Cannon or\
                            element.__class__ is block.Turret or\
                            element.__class__ is block.Shield or\
                            element.__class__ is block.TorpedoLaunch:
                        element.update(dt)

        for bullet in self.bullet:
            bullet.update_pos()
            if "Torpedo" in str(bullet.__class__):
                bullet.update(dt)

    def mouv(self, x: int, y: int, dt: float) -> None:
        """
        function managing the ship's movements
        according to the keys pressed
        """

        for line in self.objects:
            for element in line:
                if "reactor" in repr(element):
                    element.propulse(x, y, dt)
                    if self.Var.mode == "multiplayer" and self.Var.main_space_ship == self:
                        if self.last_reactor_x != x or self.last_reactor_y != y:
                            self.Var.client.send("MOUV:" + str(x) + "|" + str(y))
                            self.last_reactor_x = x
                            self.last_reactor_y = y

    def shot_cannon(self) -> None:
        for line in self.objects:
            for element in line:
                if element.__class__ is block.Cannon:
                    element.shot()

    def shot_turret(self, shot_pos=None) -> None:
        for line in self.objects:
            for element in line:
                if element.__class__ is block.Turret:
                    element.shot(shot_pos=shot_pos)

    def shot_torpedo(self, pos: tuple) -> None:
        for line in self.objects:
            for element in line:
                if element.__class__ is block.TorpedoLaunch:
                    element.shot(pos)

    def stop_shot_cannon(self) -> None:
        for line in self.objects:
            for element in line:
                if element.__class__ is block.Cannon:
                    element.stop_shot()

    def stop_shot_turret(self) -> None:
        for line in self.objects:
            for element in line:
                if element.__class__ is block.Turret:
                    element.stop_shot()

    def save(self, name: str) -> None:
        path = "resource/save/"
        extension = ".save"
        save = []
        for i in self.sprites_creation_copy:
            save.append([])
            for j in i:
                type = j[0]
                if all(j):
                    flip_x = j[1].image.flip_x
                    flip_y = j[1].image.flip_y
                else:
                    flip_x = False
                    flip_y = False
                save[-1].append((type, flip_x, flip_y))

        with open(path + name + extension, "wb") as file:
            pickle.dump(save, file)

    def load(self, name: str, bot=False) -> None:
        path = abspath("") + "\\resource\\save\\"
        path += "bot\\" if bot else ""
        extension = ".save"
        save = []

        with open(path + name + extension, "rb") as file:
            save = pickle.load(file)

        for i, line in enumerate(save):
            for j, element in enumerate(line):
                if element[0] is None:
                    self.sprites_creation_copy[i][j] = (None, None)
                else:
                    self.Var.flip_x = element[1]
                    self.Var.flip_y = element[2]
                    self.add_element(element[0], j, i)

    def delete(self):
        for line in self.objects:
            for element in line:
                if element:
                    element.delete()
        for i in range(len(self.bullet) - 1, -1, -1):
            self.bullet[i].delete()

    def set_pos(self, pos: tuple) -> None:
        if self.objects[self.pos_core[1]][self.pos_core[0]]:
            self_pos = self.get_pos()
            delta_pos = pos - self_pos
            for line in self.objects:
                for element in line:
                    if element:
                        angle = -radians(element.get_angle())
                        element.set_pos(element.get_pos() + delta_pos * sin(angle))

    def get_pos(self) -> Vec2d:
        if not self.objects[self.pos_core[1]][self.pos_core[0]]:
            return Vec2d(0, 0)
        return self.objects[self.pos_core[1]][self.pos_core[0]].get_pos()

    def set_angle(self, angle: float) -> None:
        if self.objects[self.pos_core[1]][self.pos_core[0]]:
            self_angle = self.get_angle()
            delta_angle = angle - self_angle
            for line in self.objects:
                for element in line:
                    if element:
                        element.set_angle(element.get_angle() + delta_angle)

    def get_angle(self) -> float:
        if not self.objects[self.pos_core[1]][self.pos_core[0]]:
            return 0.
        return self.objects[self.pos_core[1]][self.pos_core[0]].get_angle()

    def estimate_cost(self) -> int:
        cost = 0
        for line in self.sprites_creation_copy:
            for element in line:
                if element[0]:
                    cost += getattr(block, element[0].title().replace(" ", ""))((0, 0), self, nothing=True).COST
        return cost
