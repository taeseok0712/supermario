import game_framework
import game_world
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
mouseX,mouseY = 0,0
block_list = []
cur_select_block = 'brick'
def enter():
    global image
    image = load_image('World 1-1.png')
    global blocks
    blocks = 0

def exit():
    global image

    del (image)


def handle_events():
    events = get_events()
    global blocks
    global clickOn
    global cur_select_block
    overlap = False

    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        if event.type == SDL_KEYDOWN and event.key == SDLK_1:
            print("1")
            cur_select_block = 'brick'
        if event.type == SDL_KEYDOWN and event.key == SDLK_2:
            cur_select_block = 'random'
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
                game_world.add_objects(block_list, 1)
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
                game_world.add_objects(block_list, 1)
        else:

            pass


def draw():
    global blocks
    global cur_select_block

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
    for game_object in game_world.all_objects():
        game_object.update()
    cnt = 0

    map_data_file = open('editmap.txt', 'w')
    for i in block_list:

        map_data_file.write("Block" + " " + str(i.type) + " " + str(i.x) + " " + str(i.y) + "\n")

        if block_list.index(i) == (len(block_list) - 1):
            map_data_file.close()




def pause():
    pass


def resume():
    pass
running =True









