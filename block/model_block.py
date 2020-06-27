#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  model_block.py
#
#  Copyright 2019 Nicolas Pengov <nicolas.pengov@sfr.fr>
#


#   ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~   IMPORT
import pymunkoptions
pymunkoptions.options["debug"] = False
import pymunk
from math import pi
from pymunk import Vec2d


#   ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~   CLASS
class ModelBlock:
    """
    Class model for the different blocks
    """

    def __init__(self, pos_ship: tuple, space_ship, **kwargs):
        """
        ModelBlock class initialization function
        """

        self.space_ship = space_ship
        self.pos_ship = pos_ship

        self.life = kwargs.get('life', 1)
        self.weight = kwargs.get('weight', 1)
        self.STORAGE_MAX = kwargs.get('STORAGE_MAX', 0)
        self.CRITICAL_LIFE = kwargs.get("CRITICAL_LIFE", 0)
        self.RECV_MAX = kwargs.get("RECV_MAX", 1)
        self.COST = kwargs.get("COST", 0)

        self.storage = 0
        self.critical = False

        self.body = None
        self.shape = None

        self.pos = 0, 0
        self.angle = 0
        self.joint_side = {"top": False, "bottom": False, "left": False, "right": False}

        self.sprite = None

    def _init_(self) -> None:
        """
        function initializing certain data that can only be done
        after the creation of all objects
        """

        top = False
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

    def _set_body_shape(self, body: pymunk.Body, shape: pymunk.Shape) -> None:
        """
        Body and fitness saving function for spatial simulation
        """

        self.body = body
        self.shape = shape
        self.shape.elasticity = 0.
        self.shape.friction = .5
        self.shape.collision_type = self.space_ship.id
        self.space_ship.Var.space.add(body, shape)

    def _set_joint_side(self, top: bool, bottom: bool, left: bool, right: bool) -> None:
        """
        function saving the sides that can receive a joint
        """

        self.joint_side["top"] = top
        self.joint_side["bottom"] = bottom
        self.joint_side["left"] = left
        self.joint_side["right"] = right

    def init_pos(self, space_ship_pos: tuple, side: str, len_height: int, len_width: int) -> None:
        """
        function calculating the initial position
        """

        if side == "top":
            relativ_pos = self.pos_ship[0] - len_width / 2, self.pos_ship[1] - len_height / 2
        elif side == "left":
            self.sprite.rotation = 90
            self.body.angle = -pi / 2
            relativ_pos = self.pos_ship[1] - len_height / 2, -self.pos_ship[0] + len_width / 2
        elif side == "bottom":
            self.sprite.rotation = 180
            self.body.angle = pi
            relativ_pos = -self.pos_ship[0] + len_width / 2, -self.pos_ship[1] + len_height / 2
        elif side == "right":
            self.sprite.rotation = 270
            self.body.angle = pi / 2
            relativ_pos = -self.pos_ship[1] + len_height / 2, self.pos_ship[0] - len_width / 2

        self.set_pos((relativ_pos[0] * 32 + space_ship_pos[0], relativ_pos[1] * 32 + space_ship_pos[1]))

    def update_pos(self):
        """
        function updating the position of the object
        """

        if self.body:
            self.pos = self.body.position
            if getattr(self, "sprite", 0) != 0:
                self.sprite.x, self.sprite.y = self.body.position
        else:
            self.sprite.x, self.sprite.y = self.pos

    def update_rotation(self):
        """
        function updating the angle of the object
        """

        if self.body:
            angle = -self.body.angle * 180 / pi % 360
            self.angle = angle
            self.sprite.rotation = abs(angle)
        else:
            self.sprite.rotation = self.angle

    def set_pos(self, pos: tuple) -> None:
        """
        setter function for the object position
        """

        pos = Vec2d(pos)
        self.pos = pos
        if self.body:
            self.body.position = pos
        if self.sprite:
            self.sprite.x, self.sprite.y = pos

    def get_pos(self) -> Vec2d:
        """
        getter function for the position of the object
        """

        return Vec2d(self.pos)

    def set_angle(self, angle: float) -> None:
        """
        setter function for the angle of the object
        """

        self.angle = angle
        if self.body:
            self.body.angle = -angle / 180 * pi % (2 * pi)
        if self.sprite:
            self.sprite.rotation = angle

    def get_angle(self) -> float:
        """
        getter function for the angle of the object
        """

        return self.angle

    def delete(self):
        if self.joint_side["top"]:
            self.space_ship.Var.space.remove(self.joint_side["top"])
            self.joint_side["top"] = False
            if self.space_ship.objects[self.pos_ship[1] + 1][self.pos_ship[0]] and\
                    self.space_ship.objects[self.pos_ship[1] + 1][self.pos_ship[0]].joint_side["bottom"]:
                joint = self.space_ship.objects[self.pos_ship[1] + 1][self.pos_ship[0]].joint_side["bottom"]
                self.space_ship.Var.space.remove(joint)
                self.space_ship.objects[self.pos_ship[1] + 1][self.pos_ship[0]].joint_side["bottom"] = False
        if self.joint_side["bottom"]:
            self.space_ship.Var.space.remove(self.joint_side["bottom"])
            self.joint_side["bottom"] = False
            if self.space_ship.objects[self.pos_ship[1] - 1][self.pos_ship[0]] and\
                    self.space_ship.objects[self.pos_ship[1] - 1][self.pos_ship[0]].joint_side["top"]:
                joint = self.space_ship.objects[self.pos_ship[1] - 1][self.pos_ship[0]].joint_side["top"]
                self.space_ship.Var.space.remove(joint)
                self.space_ship.objects[self.pos_ship[1] - 1][self.pos_ship[0]].joint_side["top"] = False
        if self.joint_side["right"]:
            self.space_ship.Var.space.remove(self.joint_side["right"])
            self.joint_side["right"] = False
            if self.space_ship.objects[self.pos_ship[1]][self.pos_ship[0] + 1] and\
                    self.space_ship.objects[self.pos_ship[1]][self.pos_ship[0] + 1].joint_side["left"]:
                joint = self.space_ship.objects[self.pos_ship[1]][self.pos_ship[0] + 1].joint_side["left"]
                self.space_ship.Var.space.remove(joint)
                self.space_ship.objects[self.pos_ship[1]][self.pos_ship[0] + 1].joint_side["left"] = False
        if self.joint_side["left"]:
            self.space_ship.Var.space.remove(self.joint_side["left"])
            self.joint_side["left"] = False
            if self.space_ship.objects[self.pos_ship[1]][self.pos_ship[0] - 1] and\
                    self.space_ship.objects[self.pos_ship[1]][self.pos_ship[0] - 1].joint_side["right"]:
                joint = self.space_ship.objects[self.pos_ship[1]][self.pos_ship[0] - 1].joint_side["right"]
                self.space_ship.Var.space.remove(joint)
                self.space_ship.objects[self.pos_ship[1]][self.pos_ship[0] - 1].joint_side["right"] = False

        self.space_ship.Var.space.remove(self.body, self.shape)
        self.space_ship.objects[self.pos_ship[1]][self.pos_ship[0]] = None
        del self.sprite

    def detect_critique(self):
        if not self.critical and self.life <= self.CRITICAL_LIFE:
            self.critical = True
            return True
        else:
            return False

    def help_info(self, consumption_label, label1, response_label1, label2, response_label2):
        consumption_label.text = ""
        label1.text = ""
        response_label1.text = ""
        label2.text = ""
        response_label2.text = ""
