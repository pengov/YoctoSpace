#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  server.py
#
#  Copyright 2019 Nicolas Pengov <nicolas.pengov@sfr.fr>
#


#   ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~   IMPORT
import socket
from threading import Thread
from time import sleep


#   ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~   VARIABLE
IP = ""
PORT = 25566
clients = []
server = None
server_on = True


#   ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~   CLASS
class Client(Thread):
    def __init__(self, client, ip, port, connection_id):
        super(Client, self).__init__()
        self.connection = client
        self.IP = ip
        self.PORT = port
        self.connection_id = connection_id
        self.connected = True
        self.BUFFER_SIZE = 1024
        self.ready = False
        self.untreted_data = []
        self.data_not_fully_received = ""

        self.send("ID:" + str(self.connection_id))
        self.ship = []
        for i in range(13):
            self.ship.append([])
            for j in range(13):
                self.ship[-1].append((None, False, False))

    def close_connection(self):
        if self.connected:
            self.connection.close()
            self.connected = False

            #   delete the client
            try:
                index = clients.index(self)
                clients.pop(index)
            except ValueError:
                pass

            #    if no client so ending the server
            if len(clients) < 2:
                if len(clients) == 1:
                    clients[0].close_connection()
                print("\nServer Shutdown...")
                server.close()

    def recv(self):
        if not self.connected:
            return "Client out"
        try:
            if self.data_not_fully_received.startswith("+START+"):
                data_ = ""
                for i in range(len(self.data_not_fully_received[7:])):
                    if self.data_not_fully_received[7 + i:].startswith("+END+"):
                        self.data_not_fully_received = self.data_not_fully_received[12 + len(data_):]
                        return data_
                    else:
                        data_ += self.data_not_fully_received[7 + i]
                data = self.connection.recv(self.BUFFER_SIZE).decode()
                self.data_not_fully_received += data
                if not data:
                    self.close_connection()
                    return "Client out"
                else:
                    return self.recv()
            else:
                data = self.connection.recv(self.BUFFER_SIZE).decode()
                self.data_not_fully_received = data
                if not data:
                    self.close_connection()
                    return "Client out"
                else:
                    return self.recv()

        except ConnectionResetError:
            self.close_connection()
            return "Client out"

        except ConnectionAbortedError:
            self.close_connection()
            return "Client out"

    def send(self, data):
        if not self.connected:
            return "client out"
        try:
            data = "+START+" + data + "+END+"
            self.connection.send(data.encode())
            return ""
        except ConnectionResetError:
            self.close_connection()
            return "Client out"

    def run(self):
        while self.connected:
            if len(self.untreted_data) == 0:
                data = self.recv()
                if data:
                    self.untreted_data.append(data)
                else:
                    continue
            data = self.untreted_data.pop(0)
            if data == "Client out":
                print(f"Client out\tid: {self.connection_id}\n")
                self.close_connection()
                continue

            elif data.startswith("SHIP READY"):
                print(f"client {self.connection_id}: READY")
                self.ready = True
                if all([client.ready for client in clients]):
                    print("All client are ready.")
                    send_ship()
                    print("Ship send.")

            elif data.startswith("READY"):
                self.ready = True
                if all([client.ready for client in clients]):
                    send_all("READY")
                    print("Game start")

            elif data.startswith("SHIP:"):
                data_list = data[5:].split("|")
                i, j = int(data_list[0]), int(data_list[1])
                element = data_list[2] if data_list[2] != "None" else None
                flip_x, flip_y = bool(int(data_list[3])), bool(int(data_list[4]))
                self.ship[i][j] = (element, flip_x, flip_y)

            elif data.startswith("MOUV:") or data.startswith("PATCH:") or \
                    data.startswith("DEL:") or data.startswith("MOUSE:") or \
                    data == "CANNON_SHOT" or data == "CANNON_STOP_SHOT" or\
                    data == "TURRET_SHOT" or data == "TURRET_STOP_SHOT" or\
                    data.startswith("TORPEDO_SHOT:"):
                for client in clients:
                    if client != self:
                        client.send(data)

            else:
                raise Exception("Data Error: " + data)


#   ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~   FUNCTION
def get_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.connect(("8.8.8.8", 80))
    ip = s.getsockname()[0]
    s.close()
    return ip


def send_all(msg):
    for client in clients:
        client.send(msg)


def start_game():
    for client in clients:
        is_player_left = 1 if clients[0].connection_id == client.connection_id else 0
        client.send("START:"+str(is_player_left))


def send_ship():
    for i, line in enumerate(clients[0].ship):
        for j in range(len(line)):
            for client in clients:
                element = client.ship[i][j]
                if element[0]:
                    to_send = "SHIP:" + str(i) + "|" +\
                                        str(j) + "|" +\
                                        str(element[0]) + "|" +\
                                        str(int(element[1])) + "|" +\
                                        str(int(element[2]))
                else:
                    to_send = "SHIP:" + str(i) + "|" + str(j) + "|" + str(None) + "|" + str(0) + "|" + str(0)
                for client_to_send in clients:
                    if client_to_send != client:
                        client_to_send.send(to_send)
                sleep(0.01)


def main(*args, **kwargs):
    global server, server_on

    print("Server Starting...")
    try:
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind((IP, PORT))
        server.listen(1)
        print("Server ip: " + str(get_ip()))

    except OSError as e:
        print("Failed...")
        print("A server is already activate on this network.")
        print()
        print("ERROR:", e)
        temp = input("\nDo you still want to create the server (\"y\" for yes)\
        \nUnsupported problems can therefore be triggered:\t")
        if temp == "y":
            try:
                server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                server.bind((IP, PORT))
                server.listen(1)
                print("\n\n\nServer ip: " + str(get_ip()))
            except Exception as e:
                print("Failed...")
                print("The server can't be create.")
                print()
                print("ERROR:", e)
                return
            else:
                print("The server is online.\n")
        else:
            return
    except Exception as e:
        print("Failed...")
        print("The server can't be create.")
        print()
        print("ERROR:", e)
        return
    else:
        print("The server is online.\n")

    connection_id = 0
    while server_on:
        if len(clients) < 2:
            print("Wait for a new connection...")
            try:
                connection, (ip, port) = server.accept()
            except OSError:
                server_on = False
            else:
                new_client = Client(connection, ip, port, connection_id)
                print("A new connection was made.")
                print(f"Info of the new client:\tip: {ip}\tport: {port}\tid: {connection_id}")
                clients.append(new_client)
                clients[-1].start()
                connection_id += 1
                print()

            if len(clients) == 2:
                start_game()

    print("The server is offline.\n")


#   ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~   MAIN
if __name__ == "__main__":
    import sys
    main(*sys.argv)
    print("End of the program.")
    sys.exit(0)
