#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  client.py
#
#  Copyright 2019 Nicolas Pengov <nicolas.pengov@sfr.fr>
#


#   ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~   IMPORT
import socket
from threading import Thread
import time


#   ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~   VARIABLE
IP = "localhost"
PORT = 25566


#   ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~   CLASS
class Client(Thread):
    def __init__(self, Var, ip=None, port=None):
        super(Client, self).__init__()
        self.Var = Var
        self.IP = ip if ip else IP
        self.PORT = port if port else PORT
        self.BUFFER_SIZE = 1024
        self.id = 0
        self.is_left_player = False
        self.untreted_data = []
        self.data_not_fully_received = ""

        self.oppenent_ship = []
        for i in range(13):
            self.oppenent_ship.append([])
            for j in range(13):
                self.oppenent_ship[-1].append((None, False, False))

        try:
            self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.connection.connect((self.IP, self.PORT))
        except Exception as e:
            print(e)
            self.connected = False
        else:
            self.connected = True

    def close_connection(self):
        self.connected = False
        self.connection.close()

    def recv(self):
        if not self.connected:
            return "Server close"
        try:
            if "+END+" not in self.data_not_fully_received:
                data = self.connection.recv(self.BUFFER_SIZE).decode()
            else:
                data = "+end+"
            if not data:
                self.close_connection()
                return "Server close"
            else:
                if data != "+end+":
                    self.data_not_fully_received += data
                if self.data_not_fully_received.startswith("+START+"):
                    data = ""
                    for i in range(len(self.data_not_fully_received[7:])):
                        if self.data_not_fully_received[7 + i:].startswith("+END+"):
                            self.data_not_fully_received = self.data_not_fully_received[12 + len(data):]
                            return data
                        else:
                            data += self.data_not_fully_received[7 + i]
                    return ""
                else:
                    return ""

        except ConnectionResetError:
            self.close_connection()
            self.Var.set_scene("multiplayer menu")
            return "Server close"

        except ConnectionAbortedError:
            self.close_connection()
            return "Server close"

    def send(self, data):
        if not self.connected:
            return "Server close"
        try:
            data = "+START+" + data + "+END+"
            self.connection.send(data.encode())
            return ""
        except ConnectionResetError:
            self.close_connection()
            return "Server close"

    def send_ship(self):
        for i, line in enumerate(self.Var.main_space_ship.sprites_creation_copy):
            for j, element in enumerate(line):
                if element[0]:
                    flip_x = int(element[1].image.flip_x)
                    flip_y = int(element[1].image.flip_y)
                    to_send = str(element[0]) + "|" + str(flip_x) + "|" + str(flip_y)
                    self.send("SHIP:" + str(i) + "|" + str(j) + "|" + to_send)
                    time.sleep(0.1)
        self.send("SHIP READY")

    def run(self):
        while self.connected:
            if len(self.untreted_data) == 0:
                data = self.recv()
                if data:
                    self.untreted_data.append(data)
                else:
                    continue
            data = self.untreted_data.pop(0)
            if data == "Server close":
                self.close_connection()

            elif data.startswith("ID:"):
                self.id = int(data[3:])

            elif data.startswith("START:"):
                #   wait the "server waiting" scene to go in "creation" scene after
                #   without sleep "server waiting" scene comes after "creation" scene
                time.sleep(0.01)
                self.is_left_player = bool(int(data[6:]))
                self.Var.set_scene("creation")

            elif data.startswith("READY"):
                self.Var.set_scene("multiplayer")
                self.Var.space.set_game("multiplayer")

            elif data.startswith("SHIP:"):
                data_list = data[5:].split("|")
                i, j = int(data_list[0]), int(data_list[1])
                element = data_list[2] if data_list[2] != "None" else None
                flip_x, flip_y = bool(int(data_list[3])), bool(int(data_list[4]))
                self.oppenent_ship[i][j] = (element, flip_x, flip_y)
                if j == 12:
                    self.Var.scenes["server waiting"][1]["sprite"]["wait " + str(i)].visible = True
                if i == 12 and j == 12:
                    self.Var.to_do = "multiplayer create oppenent"
                    for i in range(13):
                        self.Var.scenes["server waiting"][1]["sprite"]["wait " + str(i)].visible = False
                    self.send("READY")

            elif data.startswith("MOUV:"):
                data_list = data[5:].split("|")
                x = int(data_list[0])
                y = int(data_list[1])
                for ship in self.Var.space.ship:
                    if ship != self.Var.main_space_ship:
                        ship.mouv(x, y)

            elif data.startswith("PATCH:"):
                scales_data = data[6:].split("&&")
                ship = [ship for ship in self.Var.space.ship if ship != self.Var.main_space_ship][0]
                for scale_data in scales_data:
                    data_list = scale_data.split("|")
                    j = int(data_list[0])
                    i = int(data_list[1])

                    x = data_list[2].split(".")
                    x = int(x[0]) + int(x[1]) / 10 ** len(x[1])
                    y = data_list[3].split(".")
                    y = int(y[0]) + int(y[1]) / 10 ** len(y[1])

                    if "e-" not in data_list[4]:
                        angle = data_list[4].split(".")
                        angle = int(angle[0]) + int(angle[1]) / 10 ** len(angle[1])
                    else:
                        angle, power = data[4].split("e-")
                        angle = angle.split(".")
                        angle = int(angle[0]) + int(angle[1]) / 10 ** len(angle[1])
                        angle *= 10 ** int(power)

                    if "e-" not in data_list[5]:
                        velo_x = data_list[5].split(".")
                        velo_x = int(velo_x[0]) + int(velo_x[1]) / 10 ** len(velo_x[1])
                    else:
                        velo_x, power = data[5].split("e-")
                        velo_x = velo_x.split(".")
                        velo_x = int(velo_x[0]) + int(velo_x[1]) / 10 ** len(velo_x[1])
                        velo_x *= 10 ** int(power)

                    if "e-" not in data_list[6]:
                        velo_y = data_list[6].split(".")
                        velo_y = int(velo_y[0]) + int(velo_y[1]) / 10 ** len(velo_y[1])
                    else:
                        velo_y, power = data[6].split("e-")
                        velo_y = velo_y.split(".")
                        velo_y = int(velo_y[0]) + int(velo_y[1]) / 10 ** len(velo_y[1])
                        velo_y *= 10 ** int(power)

                    if "e-" not in data_list[7]:
                        angu_velo = data_list[7].split(".")
                        angu_velo = int(angu_velo[0]) + int(angu_velo[1]) / 10 ** len(angu_velo[1])
                    else:
                        angu_velo, power = data[7].split("e-")
                        angu_velo = angu_velo.split(".")
                        angu_velo = int(angu_velo[0]) + int(angu_velo[1]) / 10 ** len(angu_velo[1])
                        angu_velo *= 10 ** int(power)

                    if ship.objects[i][j]:
                        ship.objects[i][j].set_pos((x, y))
                        ship.objects[i][j].set_angle(angle)
                        ship.objects[i][j].body.velocity = velo_x, velo_y
                        ship.objects[i][j].body.angular_velocity = angu_velo

            elif data.startswith("CANNON_SHOT"):
                for ship in self.Var.space.ship:
                    if ship != self.Var.main_space_ship:
                        ship.shot_cannon()

            elif data.startswith("CANNON_STOP_SHOT"):
                for ship in self.Var.space.ship:
                    if ship != self.Var.main_space_ship:
                        ship.stop_shot_cannon()

            elif data.startswith("TURRET_SHOT"):
                for ship in self.Var.space.ship:
                    if ship != self.Var.main_space_ship:
                        ship.shot_turret(shot_pos=ship.shot_pos)

            elif data.startswith("TURRET_STOP_SHOT"):
                for ship in self.Var.space.ship:
                    if ship != self.Var.main_space_ship:
                        ship.stop_shot_turret()

            elif data.startswith("TORPEDO_SHOT:"):
                data_list = data[13:].split("|")
                x = int(data_list[0])
                y = int(data_list[1])
                for ship in self.Var.space.ship:
                    if ship != self.Var.main_space_ship:
                        ship.shot_torpedo((x, y))

            elif data.startswith("DEL:"):
                data_list = data[4:].split("|")
                j = int(data_list[0])
                i = int(data_list[1])
                for ship in self.Var.space.ship:
                    if ship != self.Var.main_space_ship:
                        if "core" in str(ship.objects[i][j]):
                            ship.objects[i][j].delete(anim=True)
                            self.Var.music["sfx"]["core explosion"].play()
                        else:
                            ship.objects[i][j].delete()

            elif data.startswith("MOUSE:"):
                data_list = data[6:].split("|")
                x = int(data_list[0])
                y = int(data_list[1])
                for ship in self.Var.space.ship:
                    if ship != self.Var.main_space_ship:
                        ship.shot_pos = x, y
