# -*- coding: utf-8 -*-
#
#  load.py
#
#  Copyright 2019 Nicolas Pengov <nicolas.pengov@sfr.fr>
#


#   ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~   IMPORT
import pyglet
from pyglet.gl import glEnable, glTexParameteri, GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST


#   ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~   FUNCTION
def load_image():
    """
    Function loading the images used for the game
    """

    image = {}
    path = "resource/image/"
    extension = ".png"
    bin = pyglet.image.atlas.TextureBin()

    def load(name):
        image = pyglet.resource.image(path + name + extension)
        glEnable(GL_TEXTURE_2D)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
        return image

    def load_animation(name):
        animation = pyglet.image.load_animation(path + name + extension)
        animation.add_to_texture_bin(bin)
        glEnable(GL_TEXTURE_2D)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
        return animation

    image["background"] = load("background")
    image["icon1"] = load("icon1")
    image["icon2"] = load("icon2")
    image["black background"] = load("black_background")
    image["base turret"] = load("base_turret")
    image["battery"] = load("battery")
    image["battery evil"] = load("battery_evil")
    image["block"] = load("block")
    image["cannon"] = load("cannon")
    image["core"] = load("core")
    image["core evil"] = load("core_evil")
    image["generator"] = load("generator")
    image["generator evil"] = load("generator_evil")
    image["reactor"] = load("reactor")
    image["reactor off"] = load("reactor_off")
    image["reinforced block"] = load("reinforced_block")
    image["shield"] = load("shield")
    image["shield evil"] = load("shield_evil")
    image["shield projection"] = load("shield_projection")
    image["shield projection evil"] = load("shield_projection_evil")
    image["torpedo launch"] = load("torpedo_launch")
    image["torpedo launch load"] = load("torpedo_launch_load")
    image["torpedo launch load evil"] = load("torpedo_launch_load_evil")
    image["triangular block"] = load("triangular_block")
    image["weapon turret"] = load("weapon_turret")
    image["grid"] = load("grid")
    image["select"] = load("select")
    image["block select"] = load("block_select")
    image["block pre select"] = load("block_pre_select")
    image["turret"] = load("turret")
    image["bullet"] = load("bullet")
    image["none"] = load("none")
    image["torpedo bullet"] = load("torpedo_bullet")
    image["torpedo bullet evil"] = load("torpedo_bullet_evil")
    image["money"] = load("money")
    image["help construction"] = load("help_construction")
    image["white square"] = load("white_square")
    image["help play"] = load("help_play")
    image["help play 2"] = load("help_play_2")

    #   button image
    path += "button/"
    image["butt multiplayer off"] = load("multiplayer_off")
    image["butt multiplayer on"] = load("multiplayer_on")
    image["butt solo off"] = load("solo_off")
    image["butt solo on"] = load("solo_on")
    image["butt training off"] = load("training_off")
    image["butt training on"] = load("training_on")
    image["butt player vs bot off"] = load("player_vs_bot_off")
    image["butt player vs bot on"] = load("player_vs_bot_on")
    image["butt return off"] = load("return_off")
    image["butt return on"] = load("return_on")
    image["butt load off"] = load("load_off")
    image["butt load on"] = load("load_on")
    image["butt save off"] = load("save_off")
    image["butt save on"] = load("save_on")
    image["butt play off"] = load("play_off")
    image["butt play on"] = load("play_on")
    image["butt vertical transform off"] = load("vertical_transformation_off")
    image["butt vertical transform on"] = load("vertical_transformation_on")
    image["butt horizontal transform off"] = load("horizontal_transformation_off")
    image["butt horizontal transform on"] = load("horizontal_transformation_on")
    image["butt join off"] = load("join_off")
    image["butt join on"] = load("join_on")
    image["butt create off"] = load("create_off")
    image["butt create on"] = load("create_on")
    image["butt none on"] = load("none_on")
    image["butt keyboard off"] = load("keyboard_off")
    image["butt keyboard on"] = load("keyboard_on")
    image["butt next off"] = load("next_off")
    image["butt next on"] = load("next_on")
    image["butt previous off"] = load("previous_off")
    image["butt previous on"] = load("previous_on")
    image["butt select off"] = load("select_off")
    image["butt select on"] = load("select_on")
    image["butt trash off"] = load("trash_off")
    image["butt trash on"] = load("trash_on")
    image["butt music off"] = load("music_off")
    image["butt music on"] = load("music_on")
    print(image["butt music on"])
    #   animation image
    path = "resource/image/animation/"
    extension = ".gif"
    image["anim waiting"] = load_animation("waiting")

    return image


def load_music():
    """
    Function loading the music and sounds used for the game
    """

    path = "resource/music/"
    music = {"music": {}, "sfx": {}}

    music["music"]["menu"] = pyglet.media.load(path + 'menu.wav', streaming=True)
    music["music"]["creation"] = pyglet.media.load(path + 'creation.wav', streaming=True)
    music["music"]["fight"] = pyglet.media.load(path + 'fight.wav', streaming=True)
    music["music"]["training"] = pyglet.media.load(path + 'training.wav', streaming=True)

    path += "sfx/"
    music["sfx"]["block hit"] = pyglet.media.load(path + 'block_hit.wav', streaming=False)
    music["sfx"]["cannon shot"] = pyglet.media.load(path + 'cannon_shot.wav', streaming=False)
    music["sfx"]["core explosion"] = pyglet.media.load(path + 'core_explosion.wav', streaming=False)
    music["sfx"]["dead shield"] = pyglet.media.load(path + 'dead_shield.wav', streaming=False)
    music["sfx"]["explosion"] = pyglet.media.load(path + 'explosion.wav', streaming=False)
    music["sfx"]["reactor"] = pyglet.media.load(path + 'reactor.wav', streaming=False)
    music["sfx"]["shield hit"] = pyglet.media.load(path + 'shield_hit.wav', streaming=False)
    music["sfx"]["torpedo shot"] = pyglet.media.load(path + 'torpedo_shot.wav', streaming=False)
    music["sfx"]["turret shot"] = pyglet.media.load(path + 'turret_shot.wav', streaming=False)

    return music
