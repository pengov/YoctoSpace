#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  variable.py
#
#  Copyright 2019 Nicolas Pengov <nicolas.pengov@sfr.fr>
#


#   ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~   IMPORT
import pyglet
from client import Client


#   ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ Class
class Var:
    """
    Class that saves all global variables
    """

    #   name of the game creator
    CREATOR = "Nicolas Pengov"

    #   screen size in pixel of the computer
    PC_SIZE = 1920, 1080
    #   window size in pixel of the game
    SCREEN_SIZE = 1280, 720
    #   factor to transform the screen size to pc size
    SCALE = 1, 1
    #   maximum number of game loop per second
    FPS_MAX = 300
    #   name of the game window
    CAPTION = "YoctoSpace"
    #   boolean indicating whether the window will be set to full screen
    FULLSCREEN = False
    #   boolean indicating whether the mouse will be visible
    MOUSE_VISIBLE = True
    #   variable storing the game window
    screen = pyglet.window.Window(*SCREEN_SIZE, visible=False, vsync=False)
    #   variable storing enough to manage events
    #   it's initialized later in the main.py
    screen_event = None

    #   type of the keyboard (azert or qwerty)
    type_keyboard = "qwerty"

    #   name of the game
    GAME_NAME = "YoctoSpace"
    #   scene currently displayed on the screen
    current_scene = "menu"
    #   variable storing all scenes
    scenes = {"menu": None}
    #   currently selected game mode
    mode = None

    #   sprite of the general background
    background = None
    #   variable storing all images
    image = {}
    #   variable storing all musics and sonds
    music = {}
    #   variable storing all font for
    font = {}

    font = None

    #   for the queue of the music
    player = pyglet.media.Player()
    player.volume = 0.1
    player.loop = True
    #   true if sfx able
    sfx = True

    #   the position of the mouse
    mouse_position = 0, 0
    #   variable used for the creation of the ship to know if the selected object
    #   has received reversals in the abscissa and ordinate axis
    flip_x = False
    flip_y = False

    #   current page and the max page for load scene a ship
    page = [0, 0]
    #   name of the ship to load
    load_name = ""
    #   list of all file of ship
    list_ship_file = []

    #   variable storing the main ship
    #   i.e. the ship used by the player who started the game
    main_space_ship = None

    #   variable storing space for motion and collision management
    space = None

    #   activate the keylogger for by exemple the save a space ship with a name
    keyboard_logger = False
    key_logger = []

    money = 0
    MAX_MONEY_SOLO = 2000
    MAX_MONEY_MULTIPLAYER = 15000

    to_do = ""

    #   server
    ip = "localhost"
    port = 25566
    client = None

    @classmethod
    def init(cls) -> None:
        """
        Function initializing larger and more numerous data
        such as images, or scenes
        and also collects information that can change between computers
        """

        from resource.load import load_image, load_music
        from space import Space
        from space_ship import SpaceShip
        from init import init_scenes
        from win32api import GetSystemMetrics

        #   gets the right size of the computer screen
        if (GetSystemMetrics(0), GetSystemMetrics(1)) != cls.PC_SIZE:
            cls.PC_SIZE = GetSystemMetrics(0), GetSystemMetrics(1)
        cls.SCALE = cls.PC_SIZE[0] / cls.SCREEN_SIZE[0], cls.PC_SIZE[1] / cls.SCREEN_SIZE[1]

        #   set the window in the middle of the screen
        cls.screen.set_location(
                        round(Var.PC_SIZE[0] / 2 - Var.SCREEN_SIZE[0] / 2),
                        round(Var.PC_SIZE[1] / 2 - Var.SCREEN_SIZE[1] / 2)
                        )
        cls.screen.set_visible(True)

        #   load image, musics and sonds
        cls.image = load_image()
        cls.music = load_music()

        pyglet.font.add_file('resource/font/YoctoFont.ttf')
        cls.font = pyglet.font.load('YoctoFont')

        #   init space
        cls.space = Space(Var)

        #   create the ship
        cls.main_space_ship = SpaceShip(Var=cls)

        #   init the scenes
        init_scenes(Var)

        #   option -> keyboard language and music
        with open("resource/option.conf") as file:
            data = file.read()
            music, sfx, keyboard = data.split("\n")[:3]
            while music.endswith(" "):
                music = music[:-1]
            while sfx.endswith(" "):
                sfx = keyboard[:-1]
            while keyboard.endswith(" "):
                keyboard = keyboard[:-1]

            music = music[6:]
            sfx = sfx[4:]
            keyboard = keyboard[9:]

            if music != "True":
                Var.scenes["menu"][1]["button"]["music"].sprite.image = Var.image["butt music off"]
                cls.player.volume = 0
                Var.scenes["menu"][1]["button"]["music"].on = False

            if sfx != "True":
                cls.sfx = False
                Var.scenes["menu"][1]["button"]["sfx"].sprite.image = Var.image["butt music off"]

            if keyboard in ["azerty", "qwerty"]:
                Var.scenes["menu"][1]["label"]["keyboard"].text = "keyboard: " + keyboard
                cls.type_keyboard = keyboard

    @classmethod
    def set_scene(cls, scene: str, mode=None) -> None:
        """
        Setter function to modify the current_scene value
        """

        cls._set_music(scene)

        cls.current_scene = scene
        if mode:
            cls.mode = mode
        if scene == "creation":
            ship_cost = cls.main_space_ship.estimate_cost()
            if cls.mode == "player vs bot":
                cls.money = cls.MAX_MONEY_SOLO - ship_cost
            elif cls.mode == "multiplayer":
                cls.money = cls.MAX_MONEY_MULTIPLAYER - ship_cost
            elif cls.mode == "training":
                cls.money = 999_999 - ship_cost

            if cls.mode != "multiplayer":
                if cls.money >= 0:
                    cls.scenes["creation"][1]["label"]["money"].color = 0, 255, 0, 255
                else:
                    cls.scenes["creation"][1]["label"]["money"].color = 255, 0, 0, 255
                cls.scenes["creation"][1]["label"]["money"].text = "money: " + str(cls.money)
            else:
                cls.to_do = "multiplayer money"

            cls.main_space_ship.sprites_creation = []
            for i in range(cls.main_space_ship.SIZE_MAX[0]):
                cls.main_space_ship.sprites_creation.append([])
                for j in range(cls.main_space_ship.SIZE_MAX[1]):
                    cls.main_space_ship.sprites_creation[-1].append((None, None))

        elif scene == "join":
            cls.key_logger = []
            cls.scenes["join"][1]["label"]["enter"].text = "________________"

    @classmethod
    def start_connection(cls) -> bool:
        if cls.client:
            cls.client.close_connection()
        cls.client = Client(cls, Var.ip, Var.port)
        cls.client.start()
        if not cls.client.connected:
            return False
        else:
            return True

    @classmethod
    def create_server(cls):
        #   get the ipv4
        import socket
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        try:
            s.connect(("8.8.8.8", 80))
        except OSError:
            cls.ip = "localhost"
            cls.scenes["server waiting"][1]["label"]["ip"].text = "Server can't be create! Are you connected to a network ?"
        else:
            cls.ip = s.getsockname()[0]
            s.close()
            cls.scenes["server waiting"][1]["label"]["ip"].text = "IP: " + str(cls.ip)

            #   start the server program and connect
            from _thread import start_new_thread
            from os import system
            start_new_thread(system, ("python server.py",))
        finally:
            cls.start_connection()

    @classmethod
    def _set_music(cls, scene):
        # # breakpoint()
        # # if cls.current_scene in ("menu", "solo menu", "multiplayer menu", "join", "server waiting"):
            # # #   start music
            # # if cls.current_scene == "menu" and scene == "menu":
                # # cls.player.queue(cls.music["music"]["menu"])
                # # cls.player.play()

            # # elif scene in ("creation", "save", "load"):
                # # cls.player.queue(cls.music["music"]["creation"])
                # # cls.player.next_source()

            # # elif scene in ("player vs bot", "multiplayer"):
                # # cls.player.queue(cls.music["music"]["fight"])
                # # cls.player.next_source()

            # # elif scene == "training":
                # # cls.player.queue(cls.music["music"]["training"])
                # # cls.player.next_source()

        if scene in ("menu", "solo menu", "multiplayer menu", "join", "server waiting"):
            #   start music
            if cls.current_scene == "menu" and scene == "menu":
                cls.player.queue(cls.music["music"]["menu"])
                cls.player.play()

            elif cls.current_scene not in ("menu", "solo menu", "multiplayer menu", "join", "server waiting"):
                cls.player.queue(cls.music["music"]["menu"])
                cls.player.next_source()

        elif scene in ("creation", "save", "load"):
            if cls.current_scene not in ("creation", "save", "load"):
                cls.player.queue(cls.music["music"]["creation"])
                cls.player.next_source()

        elif scene in ("player vs bot", "multiplayer"):
            if cls.current_scene not in ("player vs bot", "multiplayer"):
                cls.player.queue(cls.music["music"]["fight"])
                cls.player.next_source()

        else:
            cls.player.queue(cls.music["music"]["training"])
            cls.player.next_source()
