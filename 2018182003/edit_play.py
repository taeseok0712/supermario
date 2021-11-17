import game_framework
import game_world
from block import Block
from pico2d import *
import ctypes

from pico2d import *
import game_framework
import game_world
from mario import Mario
from stage1BG import Stage1BG
from block import Block
name = "EditPlay"

mario = None
backGround = None


def collide(a, b):
    left_a, bottom_a, right_a, top_a = a.get_bb()
    left_b, bottom_b, right_b, top_b = b.get_bb()
    if left_a > right_b: return False
    if right_a < left_b: return False
    if top_a < bottom_b: return False
    if bottom_a > top_b: return False
    return True


def enter():
    read_file()
    print("read")
    global mario
    mario = Mario()
    game_world.add_object(mario, 1)

    global backGround
    backGround = Stage1BG()
    game_world.add_object(backGround, 0)






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
            mario.handle_event(event)


def update():
    for game_object in game_world.all_objects():
        game_object.update()



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

    obj_data_file = open('editmap.txt', "r", encoding="utf8")

    while True:
        try:
            data_obj_line = obj_data_file.readline()

            data_map_obj = data_obj_line.split()


            obj_type = data_map_obj[0]
            obj_xPos = float(data_map_obj[1])
            obj_yPos = float(data_map_obj[2])
            print(data_map_obj[1])

            global block
            block = Block(obj_type, obj_xPos, obj_yPos)
            game_world.add_object(block, 1)
        except:
            break

    obj_data_file.close()

