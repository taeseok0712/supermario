import random
import json
import os

from pico2d import *
import game_framework
import game_world
import server
from mario import Mario
from stage2BG import Stage2BG
from block import Block
name = "Stage2"
from ui import C_UI_
from Gumba import Gumba
from turtle import Turtle
import title_state
import stage2
mario = None
backGround = None





def enter():
    server.stage = 2
    if server.mario == None:
        server.mario = Mario()
        game_world.add_object(server.mario, 1)

    global backGround
    backGround = Stage2BG()
    game_world.add_object(backGround, 0)

    read_file()
    game_world.add_objects(server.blocks, 1)
    for i in server.blocks:
        i.stage = 1


    server.ui = C_UI_()
    game_world.add_object(server.ui,1)
    game_world.add_objects(server.gumba,1)


    game_world.add_objects(server.turtle, 1)

    print(server.mario)





def exit():
    game_world.clear()
    server.clear()
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
        elif event.type == SDL_KEYDOWN and event.key == SDLK_F1:
            for block in server.blocks:
                block.y += 16
        else:
            server.mario.handle_event(event)


def update():
    for game_object in game_world.all_objects():
        game_object.update()
    for coin in server.coin:
        if coin.remove:
            server.coin.remove(coin)
            print(server.coin)
            game_world.remove_object(coin)
    if server.mario.scrollX + server.mario.x > 6550 or server.ui.time < 0 or server.mario.gameEnd:
        game_framework.change_state(title_state)







def draw():
    clear_canvas()
    for game_object in game_world.all_objects():
        game_object.draw()
    update_canvas()

def collide(a, b):
    left_a, bottom_a, right_a, top_a = a.get_bb()
    left_b, bottom_b, right_b, top_b = b.get_bb()
    if left_a > right_b: return False
    if right_a < left_b: return False
    if top_a < bottom_b: return False
    if bottom_a > top_b: return False
    return True

def read_file():
    obj_xPos, obj_yPos = 0, 0
    obj_type = ""
    obj_name = ""
    data_map_obj = []

    obj_data_file = open('stage2.txt', "r", encoding="utf8")

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

        except:
            break

    obj_data_file.close()






