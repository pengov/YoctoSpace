#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  init.py
#
#  Copyright 2019 Nicolas Pengov <nicolas.pengov@sfr.fr>
#


#   ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~   IMPORT
import pyglet
from button import Button
from os.path import isfile, join
from os import listdir, remove
from time import sleep


#   ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~   FUNCTION
def init_scenes(Var) -> None:
    """
    Initializes the different scenes and records them
    """

    Var.scenes["menu"] = init_scene_menu(Var)
    Var.scenes["solo menu"] = init_scene_solo_menu(Var)
    Var.scenes["multiplayer menu"] = init_scene_multiplayer_menu(Var)
    Var.scenes["save"] = init_scene_save(Var)
    Var.scenes["load"] = init_scene_load(Var)
    Var.scenes["creation"] = init_scene_creation(Var)
    Var.scenes["training"] = init_scene_training(Var)
    Var.scenes["player vs bot"] = init_scene_player_vs_bot(Var)
    Var.scenes["join"] = init_scene_join(Var)
    Var.scenes["server waiting"] = init_scene_server_waiting(Var)
    Var.scenes["multiplayer"] = init_scene_multiplayer(Var)


def init_scene_menu(Var) -> tuple:
    batch = pyglet.graphics.Batch()
    objects = {"button": {}, "label": {}, "sprite": {}}

    objects["label"]["game name"] = pyglet.text.Label(
                        Var.GAME_NAME,
                        font_name="YoctoFont",
                        font_size=72,
                        x=Var.SCREEN_SIZE[0] // 2,
                        y=Var.SCREEN_SIZE[1] // 4 * 3,
                        anchor_x='center',
                        anchor_y='center',
                        batch=batch
                        )

    objects["label"]["keyboard"] = pyglet.text.Label(
                        "keyboard: " + Var.type_keyboard,
                        font_name='YoctoFont',
                        font_size=20,
                        x=Var.SCREEN_SIZE[0] // 2,
                        y=Var.SCREEN_SIZE[1] // 6,
                        anchor_x='center',
                        anchor_y='center',
                        batch=batch
                        )

    objects["label"]["music"] = pyglet.text.Label(
                        "music:",
                        font_name='YoctoFont',
                        font_size=20,
                        x=Var.SCREEN_SIZE[0] - Var.image["butt music on"].width,
                        y=Var.SCREEN_SIZE[1] - Var.image["butt music on"].height + 24,
                        anchor_x='center',
                        anchor_y='center',
                        batch=batch
                        )

    objects["label"]["sfx"] = pyglet.text.Label(
                        "sfx:",
                        font_name='YoctoFont',
                        font_size=20,
                        x=Var.SCREEN_SIZE[0] - Var.image["butt music on"].width,
                        y=Var.SCREEN_SIZE[1] - Var.image["butt music on"].height - 88,
                        anchor_x='center',
                        anchor_y='center',
                        batch=batch
                        )

    objects["button"]["solo"] = Button(
                        (Var.SCREEN_SIZE[0] // 4, Var.SCREEN_SIZE[1] // 5 * 2),
                        Var.image["butt solo off"],
                        Var.image["butt solo on"],
                        anchor=["center", "center"],
                        batch=batch
                        )
    objects["button"]["solo"].set_function(lambda: Var.set_scene("solo menu"))

    objects["button"]["multiplayer"] = Button(
                        (Var.SCREEN_SIZE[0] // 4 * 3, Var.SCREEN_SIZE[1] // 5 * 2),
                        Var.image["butt multiplayer off"],
                        Var.image["butt multiplayer on"],
                        anchor=["center", "center"],
                        batch=batch
                        )
    objects["button"]["multiplayer"].set_function(lambda: Var.set_scene("multiplayer menu", mode="multiplayer"))

    objects["button"]["keyboard"] = Button(
                        (Var.SCREEN_SIZE[0] // 2, Var.SCREEN_SIZE[1] // 10),
                        Var.image["butt keyboard off"],
                        Var.image["butt keyboard on"],
                        anchor=["center", "center"],
                        batch=batch
                        )

    def func():
        model = ["azerty", "qwerty"]
        Var.type_keyboard = model[model.index(Var.type_keyboard) - 1]
        objects["label"]["keyboard"].text = "keyboard: " + Var.type_keyboard
        with open("resource/option.conf", "w") as file:
            file.write(f"""music={objects["button"]["music"].on}\nsfx={Var.sfx}\nkeyboard={Var.type_keyboard}""")

    objects["button"]["keyboard"].set_function(func)

    Var.image["butt music off"].anchor_x = Var.image["butt music off"].width // 2
    Var.image["butt music off"].anchor_y = Var.image["butt music off"].height // 2
    Var.image["butt music on"].anchor_x = Var.image["butt music on"].width // 2
    Var.image["butt music on"].anchor_y = Var.image["butt music on"].height // 2

    objects["button"]["music"] = Button(
                        (Var.SCREEN_SIZE[0] - Var.image["butt music on"].width,
                            Var.SCREEN_SIZE[1] - Var.image["butt music on"].height - 32),
                        Var.image["butt music on"],
                        Var.image["butt music on"],
                        anchor=["center", "center"],
                        batch=batch
                        )
    objects["button"]["music"].on = True

    def func():
        objects["button"]["music"].on = not objects["button"]["music"].on
        if objects["button"]["music"].on:
            objects["button"]["music"].sprite.image = Var.image["butt music on"]
            Var.player.volume = 0.1
        else:
            objects["button"]["music"].sprite.image = Var.image["butt music off"]
            Var.player.volume = 0
        with open("resource/option.conf", "w") as file:
            file.write(f"""music={objects["button"]["music"].on}\nsfx={Var.sfx}\nkeyboard={Var.type_keyboard}""")

    objects["button"]["music"].set_function(func)

    objects["button"]["sfx"] = Button(
                        (Var.SCREEN_SIZE[0] - Var.image["butt music on"].width,
                            Var.SCREEN_SIZE[1] - Var.image["butt music on"].height - 144),
                        Var.image["butt music on"],
                        Var.image["butt music on"],
                        anchor=["center", "center"],
                        batch=batch
                        )

    def func():
        Var.sfx = not Var.sfx
        if Var.sfx:
            objects["button"]["sfx"].sprite.image = Var.image["butt music on"]
        else:
            objects["button"]["sfx"].sprite.image = Var.image["butt music off"]
        with open("resource/option.conf", "w") as file:
            file.write(f"""music={objects["button"]["music"].on}\nsfx={Var.sfx}\nkeyboard={Var.type_keyboard}""")

    objects["button"]["sfx"].set_function(func)

    return batch, objects


def init_scene_solo_menu(Var) -> tuple:
    batch = pyglet.graphics.Batch()
    objects = {"button": {}, "label": {}, "sprite": {}}

    objects["label"]["solo menu"] = pyglet.text.Label(
                        "Play Solo",
                        font_name='YoctoFont',
                        font_size=64,
                        x=Var.SCREEN_SIZE[0] // 2,
                        y=Var.SCREEN_SIZE[1] // 4 * 3,
                        anchor_x='center',
                        anchor_y='center',
                        batch=batch
                        )

    objects["button"]["training"] = Button(
                        (Var.SCREEN_SIZE[0] // 4, Var.SCREEN_SIZE[1] // 5 * 2),
                        Var.image["butt training off"],
                        Var.image["butt training on"],
                        anchor=["center", "center"],
                        batch=batch
                        )
    objects["button"]["training"].set_function(lambda: Var.set_scene("creation", mode="training"))

    objects["button"]["player vs bot"] = Button(
                        (Var.SCREEN_SIZE[0] // 4 * 3, Var.SCREEN_SIZE[1] // 5 * 2),
                        Var.image["butt player vs bot off"],
                        Var.image["butt player vs bot on"],
                        anchor=["center", "center"],
                        batch=batch
                        )
    objects["button"]["player vs bot"].set_function(lambda: Var.set_scene("creation", mode="player vs bot"))

    objects["button"]["return"] = Button(
                        (Var.SCREEN_SIZE[0] // 20, Var.SCREEN_SIZE[1] // 13 * 12),
                        Var.image["butt return off"],
                        Var.image["butt return on"],
                        anchor=["center", "center"],
                        batch=batch
                        )
    objects["button"]["return"].set_function(lambda: Var.set_scene("menu"))

    return batch, objects


def init_scene_multiplayer_menu(Var) -> tuple:
    batch = pyglet.graphics.Batch()
    z0 = pyglet.graphics.OrderedGroup(0)
    objects = {"button": {}, "label": {}, "sprite": {}}

    objects["label"]["multiplayer menu"] = pyglet.text.Label(
                        "Multiplayer",
                        font_name='YoctoFont',
                        font_size=64,
                        x=Var.SCREEN_SIZE[0] // 2,
                        y=Var.SCREEN_SIZE[1] // 4 * 3,
                        anchor_x='center',
                        anchor_y='center',
                        batch=batch,
                        group=z0
                        )

    objects["label"]["or"] = pyglet.text.Label(
                        "OR",
                        font_name='YoctoFont',
                        font_size=32,
                        x=Var.SCREEN_SIZE[0] // 2,
                        y=Var.SCREEN_SIZE[1] // 5 * 2,
                        anchor_x='center',
                        anchor_y='center',
                        batch=batch,
                        group=z0
                        )

    objects["label"]["party"] = pyglet.text.Label(
                        "a party",
                        font_name='YoctoFont',
                        font_size=48,
                        x=Var.SCREEN_SIZE[0] // 2,
                        y=Var.SCREEN_SIZE[1] // 15 * 4,
                        anchor_x='center',
                        anchor_y='center',
                        batch=batch,
                        group=z0
                        )

    objects["button"]["create"] = Button(
                        (Var.SCREEN_SIZE[0] // 4, Var.SCREEN_SIZE[1] // 5 * 2),
                        Var.image["butt create off"],
                        Var.image["butt create on"],
                        anchor=["center", "center"],
                        batch=batch,
                        group=z0
                        )

    def func():
        Var.create_server()
        Var.set_scene("server waiting")

    objects["button"]["create"].set_function(func)

    objects["button"]["join"] = Button(
                        (Var.SCREEN_SIZE[0] // 4 * 3, Var.SCREEN_SIZE[1] // 5 * 2),
                        Var.image["butt join off"],
                        Var.image["butt join on"],
                        anchor=["center", "center"],
                        batch=batch,
                        group=z0
                        )

    def func():
        Var.set_scene("join")
        Var.keyboard_logger = True

    objects["button"]["join"].set_function(func)

    objects["button"]["return"] = Button(
                        (Var.SCREEN_SIZE[0] // 20, Var.SCREEN_SIZE[1] // 13 * 12),
                        Var.image["butt return off"],
                        Var.image["butt return on"],
                        anchor=["center", "center"],
                        batch=batch,
                        group=z0
                        )
    objects["button"]["return"].set_function(lambda: Var.set_scene("menu"))

    return batch, objects


def init_scene_save(Var) -> tuple:
    batch = pyglet.graphics.Batch()
    z0 = pyglet.graphics.OrderedGroup(0)
    z1 = pyglet.graphics.OrderedGroup(1)
    objects = {"button": {}, "label": {}, "sprite": {}}

    objects["label"]["save name"] = pyglet.text.Label(
                        "____________",
                        font_name="YoctoFont",
                        font_size=50,
                        x=Var.SCREEN_SIZE[0] // 2,
                        y=Var.SCREEN_SIZE[1] // 2,
                        italic=True,
                        color=(191, 191, 255, 255),
                        anchor_x='center',
                        anchor_y='center',
                        batch=batch,
                        group=z1
                        )

    objects["label"]["little text"] = pyglet.text.Label(
                        "Saved Name",
                        font_name="YoctoFont",
                        font_size=64,
                        x=Var.SCREEN_SIZE[0] // 2,
                        y=Var.SCREEN_SIZE[1] // 3 * 2,
                        anchor_x='center',
                        anchor_y='center',
                        batch=batch,
                        group=z1
                        )

    objects["label"]["error"] = pyglet.text.Label(
                        "",
                        font_name="YoctoFont",
                        font_size=32,
                        x=Var.SCREEN_SIZE[0] // 2,
                        y=Var.SCREEN_SIZE[1] // 6,
                        color=(255, 0, 0, 255),
                        anchor_x='center',
                        anchor_y='center',
                        batch=batch,
                        group=z1
                        )

    objects["sprite"]["background"] = pyglet.sprite.Sprite(
                        Var.image["black background"],
                        x=0,
                        y=0,
                        batch=batch,
                        group=z0
                        )

    objects["button"]["clear"] = Button(
                        (Var.SCREEN_SIZE[0] * 12 // 15, Var.SCREEN_SIZE[1] // 2),
                        Var.image["none"],
                        Var.image["butt none on"],
                        anchor=["center", "center"],
                        batch=batch,
                        group=z1
                        )

    def func():
        Var.key_logger = []

    objects["button"]["clear"].set_function(func)

    objects["button"]["return"] = Button(
                        (Var.SCREEN_SIZE[0] // 20, Var.SCREEN_SIZE[1] // 13 * 12),
                        Var.image["butt return off"],
                        Var.image["butt return on"],
                        anchor=["center", "center"],
                        batch=batch,
                        group=z1
                        )

    def func():
        Var.keyboard_logger = False
        Var.set_scene("creation")

    objects["button"]["return"].set_function(func)

    objects["button"]["save ship"] = Button(
                        (Var.SCREEN_SIZE[0] // 2, Var.SCREEN_SIZE[1] // 3),
                        Var.image["butt save off"].get_transform(),
                        Var.image["butt save on"].get_transform(),
                        anchor=["center", "center"],
                        batch=batch,
                        group=z1
                        )

    def func():
        if not any([any([1 if j != (None,) * 2 else 0 for j in i]) for i in Var.main_space_ship.sprites_creation_copy]):
            objects["label"]["error"].text = "Nothing to save"
            return
        elif Var.key_logger == []:
            objects["label"]["error"].text = "Enter a name for save"
            return
        elif len(Var.key_logger) > 16:
            objects["label"]["error"].text = "16 characters max"
            return
        else:
            Var.keyboard_logger = False
            Var.main_space_ship.save("save_" + objects["label"]["save name"].text)
            Var.set_scene("creation")

    objects["button"]["save ship"].set_function(func)

    return batch, objects


def init_scene_load(Var) -> tuple:
    path = "resource/save"
    list_ship_file = [f for f in listdir(path) if isfile(join(path, f)) and join(path, f).endswith(".save")]
    for i in reversed(list_ship_file):
        if not i.startswith("save_"):
            list_ship_file.remove(i)
        else:
            list_ship_file[list_ship_file.index(i)] = i[5:-5]
    max_page = len(list_ship_file) // 4 + (1 if len(list_ship_file) % 4 != 0 else 0)
    Var.page[1] = max_page
    Var.list_ship_file = list_ship_file

    batch = pyglet.graphics.Batch()
    z0 = pyglet.graphics.OrderedGroup(0)
    z1 = pyglet.graphics.OrderedGroup(1)
    objects = {"button": {}, "label": {}, "sprite": {}}

    objects["label"]["title"] = pyglet.text.Label(
                        "Load a Ship",
                        font_name="YoctoFont",
                        font_size=64,
                        x=Var.SCREEN_SIZE[0] // 2,
                        y=Var.SCREEN_SIZE[1] // 5 * 4,
                        anchor_x='center',
                        anchor_y='center',
                        batch=batch,
                        group=z1
                        )

    objects["label"]["error"] = pyglet.text.Label(
                        "",
                        font_name="YoctoFont",
                        font_size=32,
                        x=Var.SCREEN_SIZE[0] // 2,
                        y=Var.SCREEN_SIZE[1] // 9,
                        color=(255, 0, 0, 255),
                        anchor_x='center',
                        anchor_y='center',
                        batch=batch,
                        group=z1
                        )

    objects["label"]["ship 0"] = pyglet.text.Label(
                        Var.list_ship_file[0] if len(Var.list_ship_file) > 0 else "",
                        font_name="YoctoFont",
                        font_size=42,
                        x=Var.SCREEN_SIZE[0] // 2 - 96,
                        y=Var.SCREEN_SIZE[1] * 3 // 5,
                        italic=True,
                        color=(191, 191, 255, 255),
                        anchor_x='right',
                        anchor_y='center',
                        batch=batch,
                        group=z1
                        )

    objects["label"]["ship 1"] = pyglet.text.Label(
                        Var.list_ship_file[1] if len(Var.list_ship_file) > 1 else "",
                        font_name="YoctoFont",
                        font_size=42,
                        x=Var.SCREEN_SIZE[0] // 2 + 96,
                        y=Var.SCREEN_SIZE[1] * 3 // 5,
                        italic=True,
                        color=(191, 191, 255, 255),
                        anchor_x='left',
                        anchor_y='center',
                        batch=batch,
                        group=z1
                        )

    objects["label"]["ship 2"] = pyglet.text.Label(
                        Var.list_ship_file[2] if len(Var.list_ship_file) > 2 else "",
                        font_name="YoctoFont",
                        font_size=42,
                        x=Var.SCREEN_SIZE[0] // 2 - 96,
                        y=Var.SCREEN_SIZE[1] * 2 // 5,
                        italic=True,
                        color=(191, 191, 255, 255),
                        anchor_x='right',
                        anchor_y='center',
                        batch=batch,
                        group=z1
                        )

    objects["label"]["ship 3"] = pyglet.text.Label(
                        Var.list_ship_file[3] if len(Var.list_ship_file) > 3 else "",
                        font_name="YoctoFont",
                        font_size=42,
                        x=Var.SCREEN_SIZE[0] // 2 + 96,
                        y=Var.SCREEN_SIZE[1] * 2 // 5,
                        italic=True,
                        color=(191, 191, 255, 255),
                        anchor_x='left',
                        anchor_y='center',
                        batch=batch,
                        group=z1
                        )

    objects["sprite"]["background"] = pyglet.sprite.Sprite(
                        Var.image["black background"],
                        x=0,
                        y=0,
                        batch=batch,
                        group=z0
                        )

    image_off = Var.image["butt select off"]
    image_off.anchor_x = image_off.width // 2
    image_off.anchor_y = image_off.height // 2
    image_on = Var.image["butt select on"]
    image_on.anchor_x = image_on.width // 2
    image_on.anchor_y = image_on.height // 2

    def func(id):
        for i in range(4):
            if i == id:
                objects["button"]["ship " + str(i)].sprite.image = image_on
            else:
                objects["button"]["ship " + str(i)].sprite.image = image_off
        Var.load_name = objects["label"]["ship " + str(id)].text

    objects["button"]["ship 0"] = Button(
                        (Var.SCREEN_SIZE[0] // 2 - 64, Var.SCREEN_SIZE[1] * 3 // 5),
                        Var.image["butt select off"],
                        Var.image["butt select on"],
                        anchor=["center", "center"],
                        batch=batch,
                        group=z1
                        )
    objects["button"]["ship 0"].set_function(func, 0)

    objects["button"]["ship 1"] = Button(
                        (Var.SCREEN_SIZE[0] // 2 + 64, Var.SCREEN_SIZE[1] * 3 // 5),
                        Var.image["butt select off"],
                        Var.image["butt select on"],
                        anchor=["center", "center"],
                        batch=batch,
                        group=z1
                        )
    objects["button"]["ship 1"].set_function(func, 1)

    objects["button"]["ship 2"] = Button(
                        (Var.SCREEN_SIZE[0] // 2 - 64, Var.SCREEN_SIZE[1] * 2 // 5),
                        Var.image["butt select off"],
                        Var.image["butt select on"],
                        anchor=["center", "center"],
                        batch=batch,
                        group=z1
                        )
    objects["button"]["ship 2"].set_function(func, 2)

    objects["button"]["ship 3"] = Button(
                        (Var.SCREEN_SIZE[0] // 2 + 64, Var.SCREEN_SIZE[1] * 2 // 5),
                        Var.image["butt select off"],
                        Var.image["butt select on"],
                        anchor=["center", "center"],
                        batch=batch,
                        group=z1
                        )
    objects["button"]["ship 3"].set_function(func, 3)

    objects["button"]["next"] = Button(
                        (Var.SCREEN_SIZE[0] * 13 // 20, Var.SCREEN_SIZE[1] // 5),
                        Var.image["butt next off"],
                        Var.image["butt next on"],
                        anchor=["center", "center"],
                        batch=batch,
                        group=z1
                        )

    def func():
        Var.page[0] += 1
        if len(Var.list_ship_file) > 4 * Var.page[0]:
            objects["label"]["ship 0"].text = Var.list_ship_file[4 * Var.page[0]]
            objects["button"]["ship 0"].sprite.visible = True
        else:
            objects["label"]["ship 0"].text = ""
            objects["button"]["ship 0"].sprite.visible = False
        if len(Var.list_ship_file) > 4 * Var.page[0] + 1:
            objects["label"]["ship 1"].text = Var.list_ship_file[4 * Var.page[0] + 1]
            objects["button"]["ship 1"].sprite.visible = True
        else:
            objects["label"]["ship 1"].text = ""
            objects["button"]["ship 1"].sprite.visible = False
        if len(Var.list_ship_file) > 4 * Var.page[0] + 2:
            objects["label"]["ship 2"].text = Var.list_ship_file[4 * Var.page[0] + 2]
            objects["button"]["ship 2"].sprite.visible = True
        else:
            objects["label"]["ship 2"].text = ""
            objects["button"]["ship 2"].sprite.visible = False
        if len(Var.list_ship_file) > 4 * Var.page[0] + 3:
            objects["label"]["ship 3"].text = Var.list_ship_file[4 * Var.page[0] + 3]
            objects["button"]["ship 3"].sprite.visible = True
        else:
            objects["label"]["ship 3"].text = ""
            objects["button"]["ship 3"].sprite.visible = False

        for i in range(4):
            objects["button"]["ship " + str(i)].sprite.image = Var.image["butt select off"]

        Var.load_name = ""

    objects["button"]["next"].set_function(func)

    objects["button"]["previous"] = Button(
                        (Var.SCREEN_SIZE[0] * 7 // 20, Var.SCREEN_SIZE[1] // 5),
                        Var.image["butt previous off"],
                        Var.image["butt previous on"],
                        anchor=["center", "center"],
                        batch=batch,
                        group=z1
                        )

    def func():
        Var.page[0] -= 1
        if len(Var.list_ship_file) > 4 * Var.page[0]:
            objects["label"]["ship 0"].text = Var.list_ship_file[4 * Var.page[0]]
            objects["button"]["ship 0"].sprite.visible = True
        else:
            objects["label"]["ship 0"].text = ""
            objects["button"]["ship 0"].sprite.visible = False
        if len(Var.list_ship_file) > 4 * Var.page[0] + 1:
            objects["label"]["ship 1"].text = Var.list_ship_file[4 * Var.page[0] + 1]
            objects["button"]["ship 1"].sprite.visible = True
        else:
            objects["label"]["ship 1"].text = ""
            objects["button"]["ship 1"].sprite.visible = False
        if len(Var.list_ship_file) > 4 * Var.page[0] + 2:
            objects["label"]["ship 2"].text = Var.list_ship_file[4 * Var.page[0] + 2]
            objects["button"]["ship 2"].sprite.visible = True
        else:
            objects["label"]["ship 2"].text = ""
            objects["button"]["ship 2"].sprite.visible = False
        if len(Var.list_ship_file) > 4 * Var.page[0] + 3:
            objects["label"]["ship 3"].text = Var.list_ship_file[4 * Var.page[0] + 3]
            objects["button"]["ship 3"].sprite.visible = True
        else:
            objects["label"]["ship 3"].text = ""
            objects["button"]["ship 3"].sprite.visible = False

        for i in range(4):
            objects["button"]["ship " + str(i)].sprite.image = Var.image["butt select off"]

        Var.load_name = ""

    objects["button"]["previous"].set_function(func)

    objects["button"]["trash"] = Button(
                        (Var.SCREEN_SIZE[0] * 3 // 4, Var.SCREEN_SIZE[1] // 5),
                        Var.image["butt trash off"],
                        Var.image["butt trash on"],
                        anchor=["center", "center"],
                        batch=batch,
                        group=z1
                        )

    def func():
        file = join("resource/save", "save_" + Var.load_name + ".save")
        if isfile(file):
            remove(file)
            sleep(1.5)
            for i in range(4):
                objects["button"]["ship " + str(i)].sprite.image = Var.image["butt select off"]
            Var.load_name = ""
            Var.set_scene("creation")
        else:
            objects["label"]["error"].text = "Select a ship to delete"

    objects["button"]["trash"].set_function(func)

    objects["button"]["return"] = Button(
                        (Var.SCREEN_SIZE[0] // 20, Var.SCREEN_SIZE[1] // 13 * 12),
                        Var.image["butt return off"],
                        Var.image["butt return on"],
                        anchor=["center", "center"],
                        batch=batch,
                        group=z1
                        )

    def func():
        for i in range(4):
            objects["button"]["ship " + str(i)].sprite.image = Var.image["butt select off"]
        Var.load_name = ""
        Var.keyboard_logger = False
        Var.set_scene("creation")

    objects["button"]["return"].set_function(func)

    objects["button"]["load ship"] = Button(
                        (Var.SCREEN_SIZE[0] // 2, Var.SCREEN_SIZE[1] // 5),
                        Var.image["butt load off"].get_transform(),
                        Var.image["butt load on"].get_transform(),
                        anchor=["center", "center"],
                        batch=batch,
                        group=z1
                        )

    def func():
        if Var.load_name == "":
            objects["label"]["error"].text = "Select a ship to load"
            return
        else:
            Var.main_space_ship.load("save_" + Var.load_name)
            for i in range(4):
                objects["button"]["ship " + str(i)].sprite.image = Var.image["butt select off"]
            Var.load_name = ""
            Var.set_scene("creation")

    objects["button"]["load ship"].set_function(func)

    return batch, objects


def init_scene_creation(Var) -> tuple:
    batch = pyglet.graphics.Batch()
    batch2 = pyglet.graphics.Batch()
    z0 = pyglet.graphics.OrderedGroup(0)
    z1 = pyglet.graphics.OrderedGroup(1)
    z2 = pyglet.graphics.OrderedGroup(2)
    z3 = pyglet.graphics.OrderedGroup(3)
    objects = {"button": {}, "label": {}, "sprite": {}}

    objects["label"]["title"] = pyglet.text.Label(
                        "Build Your Spaceship",
                        font_name='YoctoFont',
                        font_size=32,
                        x=Var.SCREEN_SIZE[0] // 11 * 3,
                        y=Var.SCREEN_SIZE[1] // 13 * 12,
                        anchor_x='center',
                        anchor_y='center',
                        italic=True,
                        batch=batch
                        )

    objects["label"]["money"] = pyglet.text.Label(
                        "money: 1500",
                        font_name="YoctoFont",
                        color=(0, 255, 0, 255),
                        font_size=16,
                        x=Var.SCREEN_SIZE[0] * 3 // 4 - 10,
                        y=25,
                        anchor_x='right',
                        anchor_y='center',
                        batch=batch
                        )

    objects["label"]["help1 title"] = pyglet.text.Label(
                        "",
                        font_size=24,
                        x=Var.SCREEN_SIZE[0] // 2 - 11 + 144,
                        y=Var.SCREEN_SIZE[1] // 15 + 6.5 * 48 + 42,
                        anchor_x='right',
                        anchor_y='center',
                        batch=batch2,
                        group=z1
                        )

    objects["label"]["help1 response"] = pyglet.text.Label(
                        "",
                        font_size=20,
                        x=Var.SCREEN_SIZE[0] // 2 - 11 + 144 + 8,
                        y=Var.SCREEN_SIZE[1] // 15 + 6.5 * 48 + 42 - 2,
                        anchor_x='left',
                        anchor_y='center',
                        batch=batch2,
                        group=z1
                        )

    objects["label"]["help2 title"] = pyglet.text.Label(
                        "",
                        font_size=24,
                        x=Var.SCREEN_SIZE[0] // 2 - 11 + 432,
                        y=Var.SCREEN_SIZE[1] // 15 + 6.5 * 48 + 42,
                        anchor_x='right',
                        anchor_y='center',
                        batch=batch2,
                        group=z1
                        )

    objects["label"]["help2 response"] = pyglet.text.Label(
                        "",
                        font_size=20,
                        x=Var.SCREEN_SIZE[0] // 2 - 11 + 432 + 8,
                        y=Var.SCREEN_SIZE[1] // 15 + 6.5 * 48 + 42 - 2,
                        anchor_x='left',
                        anchor_y='center',
                        batch=batch2,
                        group=z1
                        )

    objects["label"]["help name"] = pyglet.text.Label(
                        "",
                        font_size=20,
                        x=Var.SCREEN_SIZE[0] // 2 - 11 + 144,
                        y=Var.SCREEN_SIZE[1] // 15 + 6.5 * 48 + 246 - 2,
                        anchor_x='left',
                        anchor_y='center',
                        batch=batch2,
                        group=z1
                        )

    objects["label"]["help cost"] = pyglet.text.Label(
                        "",
                        font_size=20,
                        x=Var.SCREEN_SIZE[0] // 2 - 11 + 432 + 8,
                        y=Var.SCREEN_SIZE[1] // 15 + 6.5 * 48 + 246 - 2,
                        anchor_x='left',
                        anchor_y='center',
                        batch=batch2,
                        group=z1
                        )

    objects["label"]["help life"] = pyglet.text.Label(
                        "",
                        font_size=20,
                        x=Var.SCREEN_SIZE[0] // 2 - 11 + 144 + 8,
                        y=Var.SCREEN_SIZE[1] // 15 + 6.5 * 48 + 180 - 2,
                        anchor_x='left',
                        anchor_y='center',
                        batch=batch2,
                        group=z1
                        )

    objects["label"]["help weight"] = pyglet.text.Label(
                        "",
                        font_size=20,
                        x=Var.SCREEN_SIZE[0] // 2 - 11 + 432 + 8,
                        y=Var.SCREEN_SIZE[1] // 15 + 6.5 * 48 + 180 - 2,
                        anchor_x='left',
                        anchor_y='center',
                        batch=batch2,
                        group=z1
                        )

    objects["label"]["help storage"] = pyglet.text.Label(
                        "",
                        font_size=20,
                        x=Var.SCREEN_SIZE[0] // 2 - 11 + 144 + 8,
                        y=Var.SCREEN_SIZE[1] // 15 + 6.5 * 48 + 108 - 2,
                        anchor_x='left',
                        anchor_y='center',
                        batch=batch2,
                        group=z1
                        )

    objects["label"]["help consumption"] = pyglet.text.Label(
                        "",
                        font_size=18,
                        x=Var.SCREEN_SIZE[0] // 2 - 11 + 432 + 8,
                        y=Var.SCREEN_SIZE[1] // 15 + 6.5 * 48 + 108,
                        anchor_x='left',
                        anchor_y='center',
                        batch=batch2,
                        group=z1,
                        multiline=True,
                        width=1000
                        )

    objects["sprite"]["grid"] = pyglet.sprite.Sprite(
                        Var.image["grid"],
                        x=Var.SCREEN_SIZE[0] // 2 - 32,
                        y=Var.SCREEN_SIZE[1] // 15,
                        batch=batch,
                        group=z0
                        )

    objects["sprite"]["block pre select"] = pyglet.sprite.Sprite(
                        Var.image["block pre select"],
                        x=Var.SCREEN_SIZE[0],
                        y=Var.SCREEN_SIZE[1],
                        batch=batch,
                        group=z2
                        )

    objects["sprite"]["block select"] = pyglet.sprite.Sprite(
                        Var.image["block select"],
                        x=Var.SCREEN_SIZE[0],
                        y=Var.SCREEN_SIZE[1],
                        batch=batch,
                        group=z3
                        )

    objects["sprite"]["grid select"] = pyglet.sprite.Sprite(
                        Var.image["select"],
                        x=Var.SCREEN_SIZE[0],
                        y=Var.SCREEN_SIZE[1],
                        batch=batch,
                        group=z3
                        )

    objects["sprite"]["money"] = pyglet.sprite.Sprite(
                        Var.image["money"],
                        x=Var.SCREEN_SIZE[0] * 3 // 4,
                        y=10,
                        batch=batch,
                        group=z3
                        )

    objects["sprite"]["help construction"] = pyglet.sprite.Sprite(
                        Var.image["help construction"],
                        x=Var.SCREEN_SIZE[0] // 2 - 11,
                        y=Var.SCREEN_SIZE[1] // 15 + 6.5 * 48,
                        batch=batch2,
                        group=z0
                        )
    objects["sprite"]["help construction"].visible = False

    img = Var.image["core"].get_transform()
    img.width *= 2.5
    img.height *= 2.5

    s_width, s_height = Var.SCREEN_SIZE[0], Var.SCREEN_SIZE[1]
    b_width, b_height = img.width, img.height

    objects["sprite"]["core"] = pyglet.sprite.Sprite(
                        img,
                        x=s_width // (10 * 16 / 9),
                        y=s_height // 30 + b_height * 1.5 * 4,
                        batch=batch,
                        group=z0
                        )

    img = Var.image["block"].get_transform()
    img.width *= 2.5
    img.height *= 2.5
    objects["sprite"]["block"] = pyglet.sprite.Sprite(
                        img,
                        x=s_width // (10 * 16 / 9) + b_width * 1.5,
                        y=s_height // 30 + b_height * 1.5 * 4,
                        batch=batch,
                        group=z0
                        )

    img = Var.image["reinforced block"].get_transform()
    img.width *= 2.5
    img.height *= 2.5
    objects["sprite"]["reinforced block"] = pyglet.sprite.Sprite(
                        img,
                        x=s_width // (10 * 16 / 9) + b_width * 1.5 * 2 - 2,
                        y=s_height // 30 + b_height * 1.5 * 4,
                        batch=batch,
                        group=z0
                        )

    img = Var.image["triangular block"].get_transform()
    img.width *= 2.5
    img.height *= 2.5
    objects["sprite"]["triangular block"] = pyglet.sprite.Sprite(
                        img,
                        x=s_width // (10 * 16 / 9) + b_width * 1.5 * 3 - 2,
                        y=s_height // 30 + b_height * 1.5 * 4,
                        batch=batch,
                        group=z0
                        )

    img = Var.image["generator"].get_transform()
    img.width *= 2.5
    img.height *= 2.5
    objects["sprite"]["generator"] = pyglet.sprite.Sprite(
                        img,
                        x=s_width // (10 * 16 / 9),
                        y=s_height // 30 + b_height * 1.5 * 3,
                        batch=batch,
                        group=z0
                        )

    img = Var.image["battery"].get_transform()
    img.width *= 2.5
    img.height *= 2.5
    objects["sprite"]["battery"] = pyglet.sprite.Sprite(
                        img,
                        x=s_width // (10 * 16 / 9) + b_width * 1.5,
                        y=s_height // 30 + b_height * 1.5 * 3,
                        batch=batch,
                        group=z0
                        )

    img = Var.image["shield"].get_transform()
    img.width *= 2.5
    img.height *= 2.5
    objects["sprite"]["shield"] = pyglet.sprite.Sprite(
                        img,
                        x=s_width // (10 * 16 / 9) + b_width * 1.5 * 2 - 2,
                        y=s_height // 30 + b_height * 1.5 * 3,
                        batch=batch,
                        group=z0
                        )

    img = Var.image["reactor"].get_transform()
    img.width *= 2.5
    img.height *= 2.5
    objects["sprite"]["reactor"] = pyglet.sprite.Sprite(
                        img,
                        x=s_width // (10 * 16 / 9) + b_width * 1.5 * 3 - 2,
                        y=s_height // 30 + b_height * 1.5 * 3,
                        batch=batch,
                        group=z0
                        )

    img = Var.image["cannon"].get_transform()
    img.width *= 2.5 // 2
    img.height *= 2.5 // 2
    objects["sprite"]["cannon"] = pyglet.sprite.Sprite(
                        img,
                        x=s_width // (10 * 16 / 9) + b_width * 1.5 * 0.125,
                        y=s_height // 30 + b_height * 1.5 * 2,
                        batch=batch,
                        group=z0
                        )

    img = Var.image["base turret"].get_transform()
    img.width *= 2.5
    img.height *= 2.5
    objects["sprite"]["base turret"] = pyglet.sprite.Sprite(
                        img,
                        x=s_width // (10 * 16 / 9) + b_width * 1.5,
                        y=s_height // 30 + b_height * 1.5 * 2,
                        batch=batch,
                        group=z0
                        )

    img = Var.image["weapon turret"].get_transform()
    img.width *= 2.5
    img.height *= 2.5
    objects["sprite"]["weapon turret"] = pyglet.sprite.Sprite(
                        img,
                        x=s_width // (10 * 16 / 9) + b_width * 1.5 + 0.25 * b_width,
                        y=s_height // 30 + b_height * 1.5 * 2 + 0.25 * b_height,
                        batch=batch,
                        group=z1
                        )

    img = Var.image["torpedo launch"].get_transform()
    img.width *= 2.5
    img.height *= 2.5
    objects["sprite"]["torpedo launch"] = pyglet.sprite.Sprite(
                        img,
                        x=s_width // (10 * 16 / 9) + b_width * 1.5 * 2 - 2,
                        y=s_height // 30 + b_height * 1.5 * 2,
                        batch=batch,
                        group=z0
                        )

    img = Var.image["none"].get_transform()
    objects["sprite"]["none"] = pyglet.sprite.Sprite(
                        img,
                        x=s_width // (10 * 16 / 9) + b_width * 1.5 * 3 - 2,
                        y=s_height // 30 + b_height * 1.5 * 2,
                        batch=batch,
                        group=z0
                        )

    objects["button"]["load"] = Button(
                        (Var.SCREEN_SIZE[0] // 11 * 1.25, Var.SCREEN_SIZE[1] // 30 + b_height * 1.5),
                        Var.image["butt load off"],
                        Var.image["butt load on"],
                        anchor=["center", 0],
                        batch=batch
                        )

    def func():
        if len(Var.list_ship_file) > 4 * Var.page[0]:
            Var.scenes["load"][1]["label"]["ship 0"].text = Var.list_ship_file[4 * Var.page[0]]
            Var.scenes["load"][1]["button"]["ship 0"].sprite.visible = True
        else:
            Var.scenes["load"][1]["label"]["ship 0"].text = ""
            Var.scenes["load"][1]["button"]["ship 0"].sprite.visible = False
        if len(Var.list_ship_file) > 4 * Var.page[0] + 1:
            Var.scenes["load"][1]["label"]["ship 1"].text = Var.list_ship_file[4 * Var.page[0] + 1]
            Var.scenes["load"][1]["button"]["ship 1"].sprite.visible = True
        else:
            Var.scenes["load"][1]["label"]["ship 1"].text = ""
            Var.scenes["load"][1]["button"]["ship 1"].sprite.visible = False
        if len(Var.list_ship_file) > 4 * Var.page[0] + 2:
            Var.scenes["load"][1]["label"]["ship 2"].text = Var.list_ship_file[4 * Var.page[0] + 2]
            Var.scenes["load"][1]["button"]["ship 2"].sprite.visible = True
        else:
            Var.scenes["load"][1]["label"]["ship 2"].text = ""
            Var.scenes["load"][1]["button"]["ship 2"].sprite.visible = False
        if len(Var.list_ship_file) > 4 * Var.page[0] + 3:
            Var.scenes["load"][1]["label"]["ship 3"].text = Var.list_ship_file[4 * Var.page[0] + 3]
            Var.scenes["load"][1]["button"]["ship 3"].sprite.visible = True
        else:
            Var.scenes["load"][1]["label"]["ship 3"].text = ""
            Var.scenes["load"][1]["button"]["ship 3"].sprite.visible = False

        Var.set_scene("load")

    objects["button"]["load"].set_function(func)

    objects["button"]["save"] = Button(
                        (Var.SCREEN_SIZE[0] // 11 * 3.75, Var.SCREEN_SIZE[1] // 30 + b_height * 1.5),
                        Var.image["butt save off"],
                        Var.image["butt save on"],
                        anchor=["center", 0],
                        batch=batch
                        )

    def func():
        Var.keyboard_logger = True
        Var.set_scene("save")

    objects["button"]["save"].set_function(func)

    objects["button"]["horizontal transform"] = Button(
                        (Var.SCREEN_SIZE[0] // 11 * 1.25 - 40, Var.SCREEN_SIZE[1] // 30 + 8),
                        Var.image["butt horizontal transform off"],
                        Var.image["butt horizontal transform on"],
                        anchor=["center", 0],
                        batch=batch
                        )

    def func():
        Var.flip_x = not Var.flip_x

    objects["button"]["horizontal transform"].set_function(func)

    objects["button"]["vertical transform"] = Button(
                        (Var.SCREEN_SIZE[0] // 11 * 3.75 + 40, Var.SCREEN_SIZE[1] // 30 + 8),
                        Var.image["butt vertical transform off"],
                        Var.image["butt vertical transform on"],
                        anchor=["center", 0],
                        batch=batch
                        )

    def func():
        Var.flip_y = not Var.flip_y

    objects["button"]["vertical transform"].set_function(func)

    objects["button"]["play"] = Button(
                        (Var.SCREEN_SIZE[0] // 11 * 2.5, Var.SCREEN_SIZE[1] // 30),
                        Var.image["butt play off"],
                        Var.image["butt play on"],
                        anchor=["center", 0],
                        batch=batch
                        )

    def func():
        correct_ship = Var.main_space_ship.init()
        if correct_ship:
            if Var.mode != "multiplayer":
                Var.set_scene(Var.mode)
                Var.space.set_game(Var.mode)
            else:
                Var.client.send_ship()
                Var.set_scene("server waiting")
                #   send ready and the ship

            for space_ship in Var.space.ship[1:]:
                space_ship.delete()
            Var.space.ship = [Var.main_space_ship]
            Var.space.bot = []

            if Var.current_scene == "player vs bot":
                new_ship = Var.main_space_ship.create_bot(1)
                for ship in new_ship:
                    Var.space.ship[-1].init()

    objects["button"]["play"].set_function(func)

    objects["button"]["return"] = Button(
                        (Var.SCREEN_SIZE[0] // 20, Var.SCREEN_SIZE[1] // 13 * 12),
                        Var.image["butt return off"],
                        Var.image["butt return on"],
                        anchor=["center", "center"],
                        batch=batch
                        )

    def func():
        if Var.mode in ("training", "player vs bot"):
            Var.set_scene("solo menu")
        elif Var.mode == "multiplayer":
            Var.set_scene("multiplayer menu")
            Var.client.close_connection()

    objects["button"]["return"].set_function(func)

    return batch, objects, batch2


def init_scene_training(Var) -> tuple:
    batch = pyglet.graphics.Batch()
    z0 = pyglet.graphics.OrderedGroup(0)
    objects = {"button": {}, "label": {}, "sprite": {}}

    objects["sprite"]["help play"] = pyglet.sprite.Sprite(
                        Var.image["help play"],
                        x=Var.SCREEN_SIZE[0] - Var.image["help play"].width,
                        y=Var.SCREEN_SIZE[1] - Var.image["help play"].height,
                        batch=batch,
                        group=z0
                        )
    objects["sprite"]["help play"].opacity = 31

    objects["sprite"]["help play 2"] = pyglet.sprite.Sprite(
                        Var.image["help play 2"],
                        x=0,
                        y=0,
                        batch=batch,
                        group=z0
                        )
    objects["sprite"]["help play 2"].opacity = 31

    objects["button"]["return"] = Button(
                        (Var.SCREEN_SIZE[0] // 20, Var.SCREEN_SIZE[1] // 13 * 12),
                        Var.image["butt return off"],
                        Var.image["butt return on"],
                        anchor=["center", "center"],
                        batch=batch
                        )

    def func():
        for ship in Var.space.ship:
            ship.delete()
        Var.set_scene("creation")

    objects["button"]["return"].set_function(func)

    return batch, objects


def init_scene_player_vs_bot(Var) -> tuple:
    batch = pyglet.graphics.Batch()
    objects = {"button": {}, "label": {}, "sprite": {}}

    objects["button"]["return"] = Button(
                        (Var.SCREEN_SIZE[0] // 20, Var.SCREEN_SIZE[1] // 13 * 12),
                        Var.image["butt return off"],
                        Var.image["butt return on"],
                        anchor=["center", "center"],
                        batch=batch
                        )

    def func():
        for ship in Var.space.ship:
            ship.delete()
        Var.set_scene("creation")

    objects["button"]["return"].set_function(func)

    return batch, objects


def init_scene_join(Var) -> tuple:
    batch = pyglet.graphics.Batch()
    objects = {"button": {}, "label": {}, "sprite": {}}

    objects["label"]["title"] = pyglet.text.Label(
                        "Join a party",
                        font_name="YoctoFont",
                        font_size=72,
                        x=Var.SCREEN_SIZE[0] // 2,
                        y=Var.SCREEN_SIZE[1] // 4 * 3,
                        anchor_x='center',
                        anchor_y='center',
                        batch=batch
                        )

    objects["label"]["help"] = pyglet.text.Label(
                        "Enter the IP of the server\nexample: 192.168.0.1",
                        font_name="YoctoFont",
                        font_size=24,
                        x=Var.SCREEN_SIZE[0] // 2,
                        y=Var.SCREEN_SIZE[1] // 2,
                        anchor_x='center',
                        anchor_y='center',
                        align="center",
                        batch=batch,
                        multiline=True,
                        width=1000
                        )

    objects["label"]["enter"] = pyglet.text.Label(
                        "________________",
                        font_name="YoctoFont",
                        font_size=32,
                        color=(191, 191, 255, 255),
                        x=Var.SCREEN_SIZE[0] // 2,
                        y=Var.SCREEN_SIZE[1] // 3,
                        anchor_x='center',
                        anchor_y='center',
                        align="center",
                        batch=batch
                        )

    objects["label"]["error"] = pyglet.text.Label(
                        "",
                        font_name="YoctoFont",
                        font_size=24,
                        color=(255, 0, 0, 255),
                        x=Var.SCREEN_SIZE[0] // 2,
                        y=Var.SCREEN_SIZE[1] // 10,
                        anchor_x='center',
                        anchor_y='center',
                        align="center",
                        batch=batch
                        )

    objects["button"]["clear"] = Button(
                        (Var.SCREEN_SIZE[0] * 3 // 4, Var.SCREEN_SIZE[1] // 3),
                        Var.image["none"],
                        Var.image["butt none on"],
                        anchor=["center", "center"],
                        batch=batch
                        )

    def func():
        Var.key_logger = []
        objects["label"]["enter"].text = "________________"

    objects["button"]["clear"].set_function(func)

    objects["button"]["join"] = Button(
                        (Var.SCREEN_SIZE[0] // 2, Var.SCREEN_SIZE[1] // 5),
                        Var.image["butt join off"],
                        Var.image["butt join on"],
                        anchor=["center", "center"],
                        batch=batch
                        )

    def func():
        Var.ip = "".join(Var.key_logger)
        objects["label"]["error"].text = ""
        if Var.ip == "" or Var.ip == " " or Var.ip == ".":
            objects["label"]["error"].text = "ERROR: Enter a IP"
            return

        if Var.start_connection():
            Var.set_scene("server waiting")
            Var.keyboard_logger = False
            Var.key_logger = []
            Var.scenes["server waiting"][1]["label"]["ip"].text = "IP: " + Var.ip
        else:
            objects["label"]["error"].text = "ERROR: Party not found"
            return

    objects["button"]["join"].set_function(func)

    objects["button"]["return"] = Button(
                        (Var.SCREEN_SIZE[0] // 20, Var.SCREEN_SIZE[1] // 13 * 12),
                        Var.image["butt return off"],
                        Var.image["butt return on"],
                        anchor=["center", "center"],
                        batch=batch
                        )

    def func():
        Var.set_scene("multiplayer menu")
        Var.key_logger = []

    objects["button"]["return"].set_function(func)

    return batch, objects


def init_scene_server_waiting(Var) -> tuple:
    batch = pyglet.graphics.Batch()
    z0 = pyglet.graphics.OrderedGroup(0)
    objects = {"button": {}, "label": {}, "sprite": {}}

    objects["label"]["title"] = pyglet.text.Label(
                        "Waiting for the second player",
                        font_name="YoctoFont",
                        font_size=60,
                        x=Var.SCREEN_SIZE[0] // 2,
                        y=Var.SCREEN_SIZE[1] // 4 * 3,
                        anchor_x='center',
                        anchor_y='center',
                        batch=batch
                        )

    objects["label"]["ip"] = pyglet.text.Label(
                        "IP: " + str(Var.ip),
                        font_name="YoctoFont",
                        font_size=24,
                        x=Var.SCREEN_SIZE[0] // 2,
                        y=Var.SCREEN_SIZE[1] // 4,
                        anchor_x='center',
                        anchor_y='center',
                        batch=batch
                        )

    objects["sprite"]["waiting"] = pyglet.sprite.Sprite(
                        Var.image["anim waiting"],
                        x=Var.SCREEN_SIZE[0] // 2 - Var.image["anim waiting"].get_max_width() // 2,
                        y=Var.SCREEN_SIZE[1] // 2 - Var.image["anim waiting"].get_max_height() // 2,
                        batch=batch,
                        group=z0
                        )

    for i in range(13):
        objects["sprite"]["wait " + str(i)] = pyglet.sprite.Sprite(
                            Var.image["white square"],
                            x=Var.SCREEN_SIZE[0] // 2 + (i - 13 / 2) * 48,
                            y=Var.SCREEN_SIZE[1] // 10,
                            batch=batch,
                            group=z0
                            )
        objects["sprite"]["wait " + str(i)].visible = False

    objects["button"]["return"] = Button(
                        (Var.SCREEN_SIZE[0] // 20, Var.SCREEN_SIZE[1] // 13 * 12),
                        Var.image["butt return off"],
                        Var.image["butt return on"],
                        anchor=["center", "center"],
                        batch=batch
                        )

    def func():
        Var.client.close_connection()
        Var.set_scene("multiplayer menu")
        Var.client = None

    objects["button"]["return"].set_function(func)

    return batch, objects


def init_scene_multiplayer(Var) -> tuple:
    batch = pyglet.graphics.Batch()
    objects = {"button": {}, "label": {}, "sprite": {}}

    objects["button"]["return"] = Button(
                        (Var.SCREEN_SIZE[0] // 20, Var.SCREEN_SIZE[1] // 13 * 12),
                        Var.image["butt return off"],
                        Var.image["butt return on"],
                        anchor=["center", "center"],
                        batch=batch
                        )

    def func():
        Var.client.close_connection()
        Var.set_scene("multiplayer menu")

    objects["button"]["return"].set_function(func)

    return batch, objects
