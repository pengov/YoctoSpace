#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  event.py
#
#  Copyright 2019 Nicolas Pengov <nicolas.pengov@sfr.fr>
#


#   ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~   IMPORT
import pyglet
from pyglet import clock
from pyglet.window import key
from pyglet.window import mouse
import pymunk.pyglet_util####################################################
import block
from mutiplayer_space_ship import MultiplayerSpaceShip
from bullet import TorpedoBullet
from pyglet.gl import glScalef
from os.path import isfile, join
from os import listdir
import pymunkoptions
pymunkoptions.options["debug"] = False
draw_option = pymunk.pyglet_util.DrawOptions()


#   ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~   CLASS
class ScreenEvent:
    """
    Class not creating an object to manage the different events
     such as the keyboard or mouse,
     also taking care of the game loop
     and the elements to be displayed on the screen
    """

    def __new__(cls, screen: pyglet.window.Window, Var) -> None:
        """
        ScreenEvent class initialization function
        """

        cls.screen = screen
        cls.Var = Var

        #   create the keyboard for the detection of pressed keys
        cls.keyboard = key.KeyStateHandler()
        screen.push_handlers(cls.keyboard)

        #   told pyglet to take care of his duties
        clock.schedule_interval(cls.update, 1/cls.Var.FPS_MAX)
        cls.screen.on_draw = cls.on_draw
        cls.screen.on_mouse_press = cls.on_mouse_press
        cls.screen.on_mouse_release = cls.on_mouse_release
        cls.screen.on_mouse_motion = cls.on_mouse_motion
        cls.screen.on_mouse_drag = cls.on_mouse_drag
        cls.screen.on_key_press = cls.on_key_press
        cls.screen.on_close = cls.on_close

        cls.sprite_select = None
        cls.multiplayer_delay = 0.
        cls.MULTIPLAYER_DELAY = 1/3

    @classmethod
    def update(cls, dt: float):
        """
        Function called as many times as the FPS_MAX per second takes the function of a game loop
        Takes as parameter the time variation between its call and its last call
        Don't call pyglet takes care of launching it every time
        """

        if dt > 0.1:
            dt = 0.1

        if cls.Var.to_do:
            if cls.Var.to_do == "multiplayer money":
                if cls.Var.money >= 0:
                    cls.Var.scenes["creation"][1]["label"]["money"].color = 0, 255, 0, 255
                else:
                    cls.Var.scenes["creation"][1]["label"]["money"].color = 255, 0, 0, 255
                cls.Var.scenes["creation"][1]["label"]["money"].text = "money: " + str(cls.Var.money)

            elif cls.Var.to_do == "multiplayer create oppenent":
                ship = MultiplayerSpaceShip()
                for i, line in enumerate(cls.Var.client.oppenent_ship):
                    for j, element in enumerate(line):
                        cls.Var.flip_x = element[1]
                        cls.Var.flip_y = element[2]
                        ship.add_element(element[0], j, i)
                ship.init()

            elif type(cls.Var.to_do) == tuple:
                while cls.Var.to_do[0] == "torpedo bullet":
                    TorpedoBullet(*cls.Var.to_do[1:6])
                    cls.Var.to_do = cls.Var.to_do[6:]
                    if len(cls.Var.to_do) == 0:
                        break
            cls.Var.to_do = ""

        #   game loop for the scene "creation"
        if cls.Var.current_scene == "creation":
            #   used to surround the creation box of the ship according to the position of the mouse
            if cls.Var.SCREEN_SIZE[0] // 2 - 32 <= cls.Var.mouse_position[0] <=\
                    cls.Var.SCREEN_SIZE[0] // 2 - 32 + cls.Var.image["grid"].width and\
                    cls.Var.SCREEN_SIZE[1] // 15 <= cls.Var.mouse_position[1] <=\
                    cls.Var.SCREEN_SIZE[1] // 15 + cls.Var.image["grid"].height:
                cell_x = (cls.Var.mouse_position[0] - (cls.Var.SCREEN_SIZE[0] // 2 - 32)) // 48
                cell_y = (cls.Var.mouse_position[1] - cls.Var.SCREEN_SIZE[1] // 15) // 48
                cell_x = min(cell_x, 12)
                cell_y = min(cell_y, 12)
                cls.Var.scenes["creation"][1]["sprite"]["grid select"].x = cell_x * 48 + cls.Var.SCREEN_SIZE[0] // 2 - 32
                cls.Var.scenes["creation"][1]["sprite"]["grid select"].y = cell_y * 48 + cls.Var.SCREEN_SIZE[1] // 15
            #   if the mouse is not on any box then no contour is made
            else:
                cls.Var.scenes["creation"][1]["sprite"]["grid select"].x = cls.Var.SCREEN_SIZE[0]
                cls.Var.scenes["creation"][1]["sprite"]["grid select"].y = cls.Var.SCREEN_SIZE[1]

            #   used to surround the object selection box according to the position of the mouse
            b_width = cls.Var.image["core"].width * 2.5 * 1.5
            x = cls.Var.mouse_position[0] - cls.Var.SCREEN_SIZE[0] // (10 * 16 / 9)
            b_height = cls.Var.image["core"].height * 2.5 * 1.5
            y = cls.Var.mouse_position[1] - (cls.Var.SCREEN_SIZE[1] // 30 + b_height)
            if x % b_width - b_width / 1.5 <= 0 and\
                    y % b_height - b_height / 1.5 <= 0 and\
                    0 <= x // b_width < 4 and\
                    1 <= y // b_height < 4:
                d = 2 if x // b_width >= 2 else 0
                cls.Var.scenes["creation"][1]["sprite"]["block pre select"].x = ((x // b_width) * b_width +
                                                                                 cls.Var.SCREEN_SIZE[0] // (10 * 16 / 9) - d)
                cls.Var.scenes["creation"][1]["sprite"]["block pre select"].y = ((y // b_height) * b_height +
                                                                                 (cls.Var.SCREEN_SIZE[1] // 30 + b_height))

                name_sprite = get_name_sprite(round(x // b_width), round(y // b_height) - 1)
                name_sprite = name_sprite.title() if type(name_sprite) == str else name_sprite
                if name_sprite is not None:
                    cls.Var.scenes["creation"][1]["sprite"]["help construction"].visible = True
                    cls.Var.scenes["creation"][1]["label"]["help name"].text = name_sprite
                    element = getattr(
                                                block,
                                                name_sprite.title().replace(" ", ""))(
                                                        (0, 0),
                                                        cls.Var.main_space_ship,
                                                        nothing=True)
                    cls.Var.scenes["creation"][1]["label"]["help cost"].text = str(element.COST)
                    cls.Var.scenes["creation"][1]["label"]["help life"].text = str(element.life)
                    cls.Var.scenes["creation"][1]["label"]["help weight"].text = str(element.weight)
                    cls.Var.scenes["creation"][1]["label"]["help storage"].text = str(element.STORAGE_MAX)
                    element.help_info(
                            cls.Var.scenes["creation"][1]["label"]["help consumption"],
                            cls.Var.scenes["creation"][1]["label"]["help1 title"],
                            cls.Var.scenes["creation"][1]["label"]["help1 response"],
                            cls.Var.scenes["creation"][1]["label"]["help2 title"],
                            cls.Var.scenes["creation"][1]["label"]["help2 response"]
                            )
                else:
                    cls.Var.scenes["creation"][1]["sprite"]["help construction"].visible = False
                    cls.Var.scenes["creation"][1]["sprite"]["help construction"].visible = False
                    cls.Var.scenes["creation"][1]["label"]["help name"].text = ""
                    cls.Var.scenes["creation"][1]["label"]["help cost"].text = ""
                    cls.Var.scenes["creation"][1]["label"]["help life"].text = ""
                    cls.Var.scenes["creation"][1]["label"]["help weight"].text = ""
                    cls.Var.scenes["creation"][1]["label"]["help storage"].text = ""
                    cls.Var.scenes["creation"][1]["label"]["help consumption"].text = ""
                    cls.Var.scenes["creation"][1]["label"]["help1 title"].text = ""
                    cls.Var.scenes["creation"][1]["label"]["help1 response"].text = ""
                    cls.Var.scenes["creation"][1]["label"]["help2 title"].text = ""
                    cls.Var.scenes["creation"][1]["label"]["help2 response"].text = ""
            #   if the mouse is not on any box then no contour is made
            else:
                cls.Var.scenes["creation"][1]["sprite"]["block pre select"].x = cls.Var.SCREEN_SIZE[0]
                cls.Var.scenes["creation"][1]["sprite"]["block pre select"].y = cls.Var.SCREEN_SIZE[1]

                cls.Var.scenes["creation"][1]["sprite"]["help construction"].visible = False
                cls.Var.scenes["creation"][1]["label"]["help name"].text = ""
                cls.Var.scenes["creation"][1]["label"]["help cost"].text = ""
                cls.Var.scenes["creation"][1]["label"]["help life"].text = ""
                cls.Var.scenes["creation"][1]["label"]["help weight"].text = ""
                cls.Var.scenes["creation"][1]["label"]["help storage"].text = ""
                cls.Var.scenes["creation"][1]["label"]["help consumption"].text = ""
                cls.Var.scenes["creation"][1]["label"]["help1 title"].text = ""
                cls.Var.scenes["creation"][1]["label"]["help1 response"].text = ""
                cls.Var.scenes["creation"][1]["label"]["help2 title"].text = ""
                cls.Var.scenes["creation"][1]["label"]["help2 response"].text = ""

            #   for load look better
            path = "resource/save"
            list_ship_file = [f for f in listdir(path) if isfile(join(path, f)) and join(path, f).endswith(".save")]
            for i in reversed(list_ship_file):
                if not i.startswith("save_"):
                    list_ship_file.remove(i)
                else:
                    list_ship_file[list_ship_file.index(i)] = i[5:-5]
            max_page = len(list_ship_file) // 4 + (1 if len(list_ship_file) % 4 != 0 else 0)
            cls.Var.page[1] = max_page
            cls.Var.list_ship_file = list_ship_file

        elif cls.Var.current_scene == "save":
            scene = cls.Var.current_scene
            if len(cls.Var.key_logger) > 0:
                cls.Var.scenes[scene][1]["label"][scene + " name"].text = "".join(cls.Var.key_logger)
            else:
                cls.Var.scenes[scene][1]["label"][scene + " name"].text = "____________"

        elif cls.Var.current_scene == "load":
            if cls.Var.page[0] < cls.Var.page[1] - 1:
                cls.Var.scenes[cls.Var.current_scene][1]["button"]["next"].sprite.visible = True
            else:
                cls.Var.scenes[cls.Var.current_scene][1]["button"]["next"].sprite.visible = False

            if cls.Var.page[0] > 0:
                cls.Var.scenes[cls.Var.current_scene][1]["button"]["previous"].sprite.visible = True
            else:
                cls.Var.scenes[cls.Var.current_scene][1]["button"]["previous"].sprite.visible = False

            path = "resource/save"
            list_ship_file = [f for f in listdir(path) if isfile(join(path, f)) and join(path, f).endswith(".save")]
            for i in reversed(list_ship_file):
                if not i.startswith("save_"):
                    list_ship_file.remove(i)
                else:
                    list_ship_file[list_ship_file.index(i)] = i[5:-5]
            max_page = len(list_ship_file) // 4 + (1 if len(list_ship_file) % 4 != 0 else 0)
            cls.Var.page[1] = max_page
            cls.Var.list_ship_file = list_ship_file

        elif cls.Var.current_scene == "join":
            if any(cls.Var.key_logger):
                cls.Var.scenes[cls.Var.current_scene][1]["label"]["enter"].text = "".join(cls.Var.key_logger)

        #   game loop for all game mode
        elif cls.Var.current_scene in ("training", "player vs bot", "multiplayer"):
            #   advances the simulation of space according to the variation of time
            cls.Var.space.step(dt)
            #   updates the different elements of the game
            for ship in cls.Var.space.ship:
                ship.update(dt)
                if ship.bot:
                    ship.bot.step(dt)

            #   manages the player's movements
            if cls.Var.main_space_ship.objects[cls.Var.main_space_ship.pos_core[1]][cls.Var.main_space_ship.pos_core[0]] is not None:
                if cls.Var.type_keyboard == "azerty":
                    x = cls.keyboard[key.D] - cls.keyboard[key.Q]
                    y = cls.keyboard[key.Z] - cls.keyboard[key.S]
                elif cls.Var.type_keyboard == "qwerty":
                    x = cls.keyboard[key.D] - cls.keyboard[key.A]
                    y = cls.keyboard[key.W] - cls.keyboard[key.S]
                cls.Var.main_space_ship.mouv(x, y, dt)
            else:
                cls.Var.main_space_ship.mouv(0, 0, dt)

            if cls.Var.current_scene == "training":
                SCREEN_SIZE_X, SCREEN_SIZE_Y = cls.Var.SCREEN_SIZE
                if SCREEN_SIZE_X - cls.Var.image["help play"].width <= cls.Var.mouse_position[0] <= SCREEN_SIZE_X and\
                        SCREEN_SIZE_Y - cls.Var.image["help play"].height <= cls.Var.mouse_position[1] <= SCREEN_SIZE_Y:
                    cls.Var.scenes["training"][1]["sprite"]["help play"].opacity = 255
                else:
                    cls.Var.scenes["training"][1]["sprite"]["help play"].opacity = 31

                if cls.Var.mouse_position[0] < cls.Var.image["help play 2"].width and\
                        cls.Var.mouse_position[1] < cls.Var.image["help play 2"].height:
                    cls.Var.scenes["training"][1]["sprite"]["help play 2"].opacity = 255
                else:
                    cls.Var.scenes["training"][1]["sprite"]["help play 2"].opacity = 31

            elif cls.Var.current_scene == "multiplayer":
                cls.multiplayer_delay += dt
                if cls.multiplayer_delay >= cls.MULTIPLAYER_DELAY:
                    cls.multiplayer_delay = 0
                    data = "PATCH:"
                    for line in cls.Var.main_space_ship.objects:
                        for element in line:
                            if element:
                                pos_ship = element.pos_ship
                                pos = element.get_pos()
                                angle = element.get_angle()
                                velocity = element.body.velocity
                                angular_velocity = element.body.angular_velocity
                                data += str(
                                    pos_ship[0]) + "|" +\
                                    str(pos_ship[1]) + "|" +\
                                    str(round(pos[0], 1)) + "|" +\
                                    str(round(pos[1], 1)) + "|" +\
                                    str(round(angle, 1)) + "|" +\
                                    str(round(velocity[0], 1)) + "|" +\
                                    str(round(velocity[1], 1)) + "|" +\
                                    str(round(angular_velocity, 1)) + "&&"
                    if data != "PATCH:":
                        cls.Var.client.send(data[:-2])
                        cls.Var.client.send("MOUSE:" + str(cls.Var.mouse_position[0]) + "|" + str(cls.Var.mouse_position[1]))

    @classmethod
    def on_draw(cls):
        """
        Function in charge of drawing the different elements on the screen
        Don't call pyglet takes care of launching it every time
        """
        cls.screen.clear()
        cls.Var.background.draw()

        if cls.Var.current_scene in ("save", "load"):
            cls.Var.scenes["creation"][0].draw()
            cls.Var.main_space_ship.batch_creation.draw()
        cls.Var.scenes[cls.Var.current_scene][0].draw()

        if cls.Var.current_scene == "creation":
            cls.Var.main_space_ship.batch_creation.draw()
            cls.Var.scenes[cls.Var.current_scene][2].draw()

        elif cls.Var.current_scene in ("training", "player vs bot", "multiplayer"):
            for ship in cls.Var.space.ship:
                ship.batch.draw()
            #   pymunk debug
            # # cls.Var.space.debug_draw(draw_option)

    @classmethod
    def on_mouse_press(cls, x_mouse, y_mouse, button, modifiers):
        """
        Function launched when a mouse click is made
        Takes as argument the position of the click the clicked button and modifies them applied to it
        Don't call pyglet takes care of launching it every time
        """

        if cls.Var.FULLSCREEN:
            x_mouse = round(x_mouse * cls.Var.SCREEN_SIZE[0] / cls.Var.PC_SIZE[0])
            y_mouse = round(y_mouse * cls.Var.SCREEN_SIZE[1] / cls.Var.PC_SIZE[1])

        #   checks if the click is not on a button in the window
        if button is mouse.LEFT:
            for button_ in cls.Var.scenes[cls.Var.current_scene][1]["button"].values():
                button_.click((x_mouse, y_mouse))

        if cls.Var.current_scene == "creation":
            #   checks if the click is not on a spaceship creation box if yes places the selected block on it
            if cls.Var.SCREEN_SIZE[0] // 2 - 32 <= x_mouse <=\
                    cls.Var.SCREEN_SIZE[0] // 2 - 32 + cls.Var.image["grid"].width and\
                    cls.Var.SCREEN_SIZE[1] // 15 <= y_mouse <=\
                    cls.Var.SCREEN_SIZE[1] // 15 + cls.Var.image["grid"].height:
                cell_x = (x_mouse - (cls.Var.SCREEN_SIZE[0] // 2 - 32)) // 48
                cell_y = (y_mouse - cls.Var.SCREEN_SIZE[1] // 15) // 48
                cell_x = min(cell_x, 12)
                cell_y = min(cell_y, 12)
                cls.Var.scenes["creation"][1]["sprite"]["grid select"].x = cell_x * 48 + cls.Var.SCREEN_SIZE[0] // 2 - 32
                cls.Var.scenes["creation"][1]["sprite"]["grid select"].y = cell_y * 48 + cls.Var.SCREEN_SIZE[1] // 15

                if button is mouse.RIGHT:
                    if cls.sprite_select is None:
                        for i in range(cls.Var.main_space_ship.SIZE_MAX[0]):
                            for j in range(cls.Var.main_space_ship.SIZE_MAX[1]):
                                cls.Var.main_space_ship.add_element(None, i, j)
                    else:
                        cls.Var.main_space_ship.add_element(None, cell_x, cell_y)
                elif button is mouse.LEFT:
                    cls.Var.main_space_ship.add_element(cls.sprite_select, cell_x, cell_y)
            #   otherwise hide the image of the selected element
            else:
                cls.Var.scenes["creation"][1]["sprite"]["grid select"].x = cls.Var.SCREEN_SIZE[0]
                cls.Var.scenes["creation"][1]["sprite"]["grid select"].y = cls.Var.SCREEN_SIZE[1]

            #   checks if the click is not on an item selection box if yes then selects it
            b_width = cls.Var.image["core"].width * 2.5 * 1.5
            x = x_mouse - cls.Var.SCREEN_SIZE[0] // (10 * 16 / 9)
            b_height = cls.Var.image["core"].height * 2.5 * 1.5
            y = y_mouse - (cls.Var.SCREEN_SIZE[1] // 30 + b_height)
            if x % b_width - b_width / 1.5 <= 0 and\
                    y % b_height - b_height / 1.5 <= 0 and\
                    0 <= x // b_width < 4 and\
                    1 <= y // b_height < 4:
                d = 2 if x // b_width >= 2 else 0
                cls.Var.scenes["creation"][1]["sprite"]["block select"].x = (x // b_width) * b_width +\
                    cls.Var.SCREEN_SIZE[0] // (10 * 16 / 9) - d
                cls.Var.scenes["creation"][1]["sprite"]["block select"].y = (y // b_height) * b_height +\
                    (cls.Var.SCREEN_SIZE[1] // 30 + b_height)
                cls.sprite_select = get_name_sprite(round(x // b_width), round(y // b_height) - 1)

        elif cls.Var.current_scene in ("training", "player vs bot", "multiplayer"):
            if cls.Var.main_space_ship.objects[cls.Var.main_space_ship.pos_core[1]][cls.Var.main_space_ship.pos_core[0]] is not None:
                if button == mouse.LEFT:
                    cls.Var.main_space_ship.shot_cannon()
                    if cls.Var.current_scene == "multiplayer":
                        cls.Var.client.send("CANNON_SHOT")
                elif button == mouse.RIGHT:
                    if modifiers in (key.MOD_SHIFT, key.MOD_SHIFT + key.MOD_CAPSLOCK, key.MOD_SHIFT + key.MOD_NUMLOCK, key.MOD_SHIFT + key.MOD_CAPSLOCK + key.MOD_NUMLOCK):
                        cls.Var.main_space_ship.shot_torpedo((x_mouse, y_mouse))
                        if cls.Var.current_scene == "multiplayer":
                            cls.Var.client.send("TORPEDO_SHOT:" + str(x_mouse) + "|" + str(y_mouse))
                    else:
                        cls.Var.main_space_ship.shot_turret()
                        cls.Var.mouse_position = x_mouse, y_mouse
                        if cls.Var.current_scene == "multiplayer":
                            cls.Var.client.send("TURRET_SHOT")

    @classmethod
    def on_mouse_release(cls, x_mouse, y_mouse, button, modifiers):
        """
        Function called when a click is released
        Takes as argument the position of the click taken on the clicked button and modifies them applied to it.
        Don't call pyglet takes care of launching it every time
        """

        if cls.Var.FULLSCREEN:
            x_mouse = round(x_mouse * cls.Var.SCREEN_SIZE[0] / cls.Var.PC_SIZE[0])
            y_mouse = round(y_mouse * cls.Var.SCREEN_SIZE[1] / cls.Var.PC_SIZE[1])

        #   release the clicked buttons
        if button is mouse.LEFT:
            for button_ in cls.Var.scenes[cls.Var.current_scene][1]["button"].values():
                button_.reset()

        if cls.Var.current_scene in ("training", "player vs bot", "multiplayer"):
            if button == mouse.LEFT:
                cls.Var.main_space_ship.stop_shot_cannon()
                if cls.Var.current_scene == "multiplayer":
                    cls.Var.client.send("CANNON_STOP_SHOT")
            elif button == mouse.RIGHT:
                # # if not modifiers == 16 + key.MOD_SHIFT:
                cls.Var.main_space_ship.stop_shot_turret()
                if cls.Var.current_scene == "multiplayer":
                    cls.Var.client.send("TURRET_STOP_SHOT")

    @classmethod
    def on_mouse_motion(cls, x, y, dx, dy):
        """
        Function called when a mouse moves
        Takes as argument the position of the mouse and the variation of it
        Don't call pyglet takes care of launching it every time
        """

        if cls.Var.FULLSCREEN:
            x = round(x * cls.Var.SCREEN_SIZE[0] / cls.Var.PC_SIZE[0])
            y = round(y * cls.Var.SCREEN_SIZE[1] / cls.Var.PC_SIZE[1])

        cls.Var.mouse_position = x, y

    @classmethod
    def on_mouse_drag(cls, x, y, dx, dy, buttons, modifiers):
        """
        Function called when a mouse moves and clicked
        Takes as argument the position of the mouse and the variation of it
        the buttons clicked and modifiers
        Don't call pyglet takes care of launching it every time
        """

        if cls.Var.FULLSCREEN:
            x = round(x * cls.Var.SCREEN_SIZE[0] / cls.Var.PC_SIZE[0])
            y = round(y * cls.Var.SCREEN_SIZE[1] / cls.Var.PC_SIZE[1])

        cls.Var.mouse_position = x, y

    @classmethod
    def on_key_press(cls, symbol, modifiers):
        if key.symbol_string(symbol) == "ESCAPE":
            breakpoint()  ######################################################################
        if key.symbol_string(symbol) == "F11":
            cls.Var.FULLSCREEN = not cls.Var.FULLSCREEN
            cls.Var.screen.set_fullscreen(cls.Var.FULLSCREEN)
            if cls.Var.FULLSCREEN:
                glScalef(*cls.Var.SCALE, 1.0)
            else:
                glScalef(1/cls.Var.SCALE[0], 1/cls.Var.SCALE[1], 1.0)

        if cls.Var.keyboard_logger:
            if key.symbol_string(symbol) == "BACKSPACE":
                if len(cls.Var.key_logger) > 0:
                    cls.Var.key_logger.pop()
                if len(cls.Var.key_logger) == 0 and cls.Var.current_scene == "join":
                    cls.Var.scenes["join"][1]["label"]["enter"].text = "________________"
            elif key.symbol_string(symbol) in "AZERTYUIOPQSDFGHJKLMWXCVBN":
                if modifiers in (key.MOD_SHIFT, key.MOD_CAPSLOCK, key.MOD_SHIFT + key.MOD_NUMLOCK, key.MOD_CAPSLOCK + key.MOD_NUMLOCK):
                    cls.Var.key_logger.append(key.symbol_string(symbol).upper())
                else:
                    cls.Var.key_logger.append(key.symbol_string(symbol).lower())
            elif key.symbol_string(symbol) in"NUM_" + "NUM_".join(("0", "1", "2", "3", "4", "5", "6", "7", "8", "9")):
                cls.Var.key_logger.append(key.symbol_string(symbol)[-1])
            elif key.symbol_string(symbol) == "SPACE":
                cls.Var.key_logger.append(" ")
            elif key.symbol_string(symbol) in ("COMMA", "NUM_DECIMAL") or\
                    key.symbol_string(symbol) == "SEMICOLON" and\
                    modifiers in (key.MOD_SHIFT, key.MOD_CAPSLOCK, key.MOD_SHIFT + key.MOD_NUMLOCK, key.MOD_CAPSLOCK + key.MOD_NUMLOCK):
                cls.Var.key_logger.append(".")
            elif key.symbol_string(symbol) == "UNDERSCORE":
                cls.Var.key_logger.append("_")

    @classmethod
    def on_close(cls):
        if cls.Var.client is not None:
            cls.Var.client.close_connection()
        exit()


#   ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~   FUNCTION
def get_name_sprite(cell_x: int, cell_y: int) -> str:
    """
    Function that returns the type of element according to its position expressed in cell
    """

    liste = [
                ["cannon", "turret", "torpedo launch", None],
                ["generator", "battery", "shield", "reactor"],
                ["core", "block", "reinforced block", "triangular block"]
                ]
    return liste[cell_y][cell_x]
