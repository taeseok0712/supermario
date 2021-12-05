import random
import json
import os

from pico2d import *
import game_framework
import game_world
import server
from mario import Mario
from stage1BG import Stage1BG
from block import Block
name = "MainState"

mario = None
backGround = None





def enter():

    server.mario = Mario()
    game_world.add_object(server.mario, 1)

    global backGround
    backGround = Stage1BG()
    game_world.add_object(backGround, 0)

    read_file()




def exit():
    game_world.clear()

def pause():
    pass


def resume():
    pass


def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
                game_framework.quit()
        else:
            server.mario.handle_event(event)


def update():
    for game_object in game_world.all_objects():
        game_object.update()

    # fill here for collision check









def draw():
    clear_canvas()
    for game_object in game_world.all_objects():
        game_object.draw()
    update_canvas()

def read_file():
    obj_xPos, obj_yPos = 0, 0
    obj_type = ""
    obj_name = ""
    data_map_obj = []

    obj_data_file = open('stage1.txt', "r", encoding="utf8")

    while True:
        try:
            data_obj_line = obj_data_file.readline()

            data_map_obj = data_obj_line.split()


            obj_type = data_map_obj[0]
            obj_xPos = float(data_map_obj[1])
            obj_yPos = float(data_map_obj[2])



            global blocks
            blocks = Block(obj_type, obj_xPos, obj_yPos)
            server.blocks.append(Block(obj_type, obj_xPos, obj_yPos))
            game_world.add_object(blocks, 0)
        except:
            break

    obj_data_file.close()






