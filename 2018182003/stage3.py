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
from cupa import Cupa
from Stone import Stone
import stage2
import load_state
mario = None
backGround = None

flag = False
bossflag = False
Ending = False
BGM = None
timer = 50
def enter():

    global bossflag
    global Ending
    global timer
    global BGM
    BGM = load_music('30 - Castle of Koopa.mp3')
    BGM.set_volume(64)
    BGM.repeat_play()

    server.stage = 3
    server.mario = Mario()
    game_world.add_object(server.mario, 1)
    server.mario.mario = server.state
    global backGround
    backGround = Stage2BG()
    game_world.add_object(backGround, 0)


    server.stone.append(Stone(1162, 493))
    server.stone.append(Stone(400, 493))
    server.stone.append(Stone(500, 493))
    server.stone.append(Stone(600, 493))
    server.stone.append(Stone(3016, 237))
    server.stone.append(Stone(3195, 237))
    server.stone.append(Stone(3439, 237))
    game_world.add_objects(server.stone, 1)

    server.turtle.append(Turtle(4084, 64))
    server.gumba.append(Gumba(2031, 64))
    game_world.add_objects(server.turtle, 1)
    game_world.add_objects(server.gumba, 1)
    server.cupa.append(Cupa(5457, 160))
    game_world.add_objects(server.cupa, 1)
    read_file()
    game_world.add_objects(server.blocks, 1)
    for i in server.blocks:
        i.stage = 2
    server.ui = C_UI_()
    game_world.add_object(server.ui, 1)







def exit():
    global BGM
    BGM = None
    server.state = server.mario.mario
    game_world.clear()
    server.clear()
    global flag
    global bossflag
    global timer
    flag = False
    bossflag = False
    timer = 50


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
        elif event.type == SDL_KEYDOWN and event.key == SDLK_UP and flag:

            game_framework.change_state(stage2)
        elif event.type == SDL_KEYDOWN and event.key == SDLK_F1:

            print(server.mario.scrollX ," ",server.mario.x)
        else:
            server.mario.handle_event(event)


def update():
    global flag
    global bossflag
    global timer

    for game_object in game_world.all_objects():
        game_object.update()
    for coin in server.coin:
        if coin.remove:
            server.coin.remove(coin)
            print(server.coin)
            game_world.remove_object(coin)

    if server.mario != None:
        if (server.ui.time < 0 or server.mario.gameEnd) :
            game_framework.change_state(load_state)
    if server.mario != None:
        if server.mario.scrollX + server.mario.x > 6550 and server.mario != None:

            game_framework.change_state(load_state)
            server.stage = 3
    if server.mario != None:
        if server.mario.scrollX + server.mario.x > 4870 and not bossflag:
            server.mario.scrollX = 4800
            server.mario.x = 50
            bossflag = True
    for block in server.blocks:
        if block.type == 'pipe_RU':
            if collide(block,server.mario):
                flag = True
    if flag:
        timer -= 1
        for block in server.blocks:
            if block.type == 'hard_brick':
                game_world.remove_object(block)
                server.blocks.remove(block)

    if flag and timer < 0:
        server.Game_End = True
        game_framework.change_state(load_state)
    print(timer)









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

    obj_data_file = open('stage3.txt', "r", encoding="utf8")

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





