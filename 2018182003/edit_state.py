import game_framework
import game_world
import edit_play
from block import Block
from pico2d import *
import ctypes

class Point(ctypes.Structure):
    _fields_ = [("x", ctypes.c_int),
                ("y", ctypes.c_int)]
CANVAS_HEIGHT =600



name = "EditState"
image = None
clickOn = False
saveOn = False
mouseX,mouseY = 0,0

cur_select_block = 'brick'
def enter():
    global image
    image = load_image('World 1-1.png')

    global block_list
    block_list = []


def exit():
    global image
    global block_list
    if saveOn:
        map_data_file = open('editmap.txt', 'w')
        for i in block_list:

            map_data_file.write(str(i.type) + " " + str(i.x) + " " + str(i.y) + "\n")

            if block_list.index(i) == (len(block_list) - 1):
                map_data_file.close()
    del (image)
    del (block_list)


def handle_events():
    events = get_events()

    global clickOn
    global saveOn
    global cur_select_block
    global block_list
    overlap = False

    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        if event.type == SDL_KEYDOWN and event.key == SDLK_1:
            cur_select_block = 'brick'
        if event.type == SDL_KEYDOWN and event.key == SDLK_2:
            cur_select_block = 'random'
        if event.type == SDL_KEYDOWN and event.key == SDLK_3:
            cur_select_block = 'pipe_LB'
        if event.type == SDL_KEYDOWN and event.key == SDLK_4:
            cur_select_block = 'pipe_LU'
        if event.type == SDL_KEYDOWN and event.key == SDLK_5:
            cur_select_block = 'pipe_RB'
        if event.type == SDL_KEYDOWN and event.key == SDLK_6:
            cur_select_block = 'pipe_RU'
        if event.type == SDL_KEYDOWN and event.key == SDLK_s:
            saveOn = True

        if event.type == SDL_MOUSEBUTTONDOWN:
            clickOn = True
            mouseX, mouseY = event.x, CANVAS_HEIGHT - 1 - event.y
            mouseX, mouseY = setPos(mouseX, mouseY, 32)
            for i in block_list:
                if i.x == mouseX and i.y == mouseY:
                    overlap = True
                    break
                else:
                    overlap = False
            if not overlap:
                block_list.append(Block(cur_select_block, mouseX, mouseY))
                game_world.add_object(Block(cur_select_block, mouseX, mouseY), 1)
        if event.type == SDL_MOUSEBUTTONUP:
            clickOn = False

        if event.type ==SDL_MOUSEMOTION and clickOn:
            print(clickOn)
            mouseX, mouseY = event.x, CANVAS_HEIGHT - 1 - event.y
            mouseX, mouseY = setPos(mouseX, mouseY, 32)
            for i in block_list:
                if i.x == mouseX and i.y == mouseY:
                    overlap = True
                    break
                else:
                    overlap = False
            if not overlap:
                block_list.append(Block(cur_select_block, mouseX, mouseY))
                game_world.add_object(Block(cur_select_block, mouseX, mouseY), 1)
        elif event.type == SDL_KEYDOWN and event.key == SDLK_F5:
            game_framework.change_state(edit_play)
        else:

            pass


def draw():
    clear_canvas()
    for game_object in game_world.all_objects():
        game_object.draw()

    update_canvas()





def setPos(x,y,size):
    px,py = 0,0
    if x%size > size/2:
        px = x+ size- x%size
    elif x%size <= size/2:
        px = x - x%size
    if y%size > size/2:
        py = y+ size- y%size
    elif y%size <= size/2:
        py = y - y%size

    print(px,py)
    return px,py




def update():
    pass
    cnt = 0





def pause():
    pass


def resume():
    pass
running =True









