from pico2d import *
import random
from C_mario import mario
from C_state import state
from C_state import Mario_state
from C_state import state_block
from C_block import Block
from C_mush import cMushRoom
from C_Stage1_Back_Ground import C_Stage1_Bk
import game_framework
import title_state
from C_UI import C_UI_
from C_Ground import Ground
name = "MainState"

def collide(a,b):
    left_a , bottom_a , right_a , top_a = a.get_hitbox()
    left_b, bottom_b, right_b, top_b = b.get_hitbox()

    if left_a > right_b: return False
    if right_a < left_b: return False
    if top_a < bottom_b: return False
    if bottom_a > top_b: return False
    return True

def is_Top(a,b):
    # a player # b box
    left_a, bottom_a, right_a, top_a = a.get_hitbox()
    left_b, bottom_b, right_b, top_b = b.get_hitbox()
    if top_a > top_b : return True


def handle_events():

    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()

        if event.type == SDL_KEYUP and event.key == SDLK_RIGHT:
            if (player.move_dir == 1):
                player.is_move = False
                player.state = state.S_idle
        if event.type == SDL_KEYUP and event.key == SDLK_LEFT:
            if(player.move_dir == -1):
                player.is_move = False
                player.state = state.S_idle
        if event.type == SDL_KEYDOWN and event.key == SDLK_RIGHT:
            player.state = state.S_move

            player.is_move = True
            player.dirction = 1
            player.move_dir = 1
        if event.type == SDL_KEYDOWN and event.key == SDLK_LEFT:
            player.state = state.S_move
            player.is_move = True
            player.dirction = 2
            player.move_dir = -1
        if event.type == SDL_KEYDOWN and event.key == SDLK_c:
            player.state = state.S_jump
            player.jump_charge = True
            player.jump_on = True


        if event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.change_state(title_state)

        if event.type == SDL_KEYUP and event.key == SDLK_c:
            player.jump_charge = False

# initialization code

def enter():

    global player
    global Ui
    global stage1_Bk
    global Platform
    global block
    global blocks
    global Grounds

    global Mushrooms
    player = mario()
    stage1_Bk = C_Stage1_Bk()

    Mushrooms = []
    Ui =C_UI_()
    platform_list=['random',900,300,'random',1500,300]

    Platform =[Block('random',200,200),Block('brick',500,200),Block('brick',700,200)]
    Grounds =[Ground(1104)]



def exit():
    global player , random_b ,stage1_Bk,Grounds,Platform,Mushrooms
    del (player)
    del (Platform)
    del (Grounds)
    del (stage1_Bk)
    global Mushrooms
def update():

    for block in Platform:
        if collide(player, block):
            block.is_coll = True
            if is_Top(player,block):
                player.jump_on = False
                player.Coll_y = block.y + block.size_y

            if (player.Drop == False):


                block.is_hit = True
                player.Drop = True
                player.is_Coll = True
                player.jump_on = False
                player.jump_accel = 0
                if (block.type == 'brick' and player.M_state == Mario_state.Super_mario):
                    Platform.remove(block)
                if(block.type == 'random' and block.state == state_block.S_Idle):
                    Mushrooms.append(cMushRoom(block.x ,block.y+block.size_y))

        else:
            player.is_Coll = False

    for Mush in Mushrooms:
        if collide(player, Mush):
            Mushrooms.remove(Mush)
            if player.M_state ==Mario_state.mario:
                player.M_state = Mario_state.Growing
                player.size_y = 64
                player.y += 16


    for ground in Grounds:
        if collide(player, ground):
            player.is_Coll = True
            player.Coll_y = 80

    for block in Platform:
        block.update(player.scroll_x)
    for ground in Grounds:
        ground.update(player.scroll_x)
    player.update()
    for Mush in Mushrooms:
        Mush.update(player.scroll_x)
    stage1_Bk.update(player.scroll_x)
    Ui.update()


def draw():
    clear_canvas()
    stage1_Bk.draw()
    player.draw()
    for block in Platform:
        block.draw()
    for ground in Grounds:
        ground.draw()
    Ui.draw()
    for Mush in Mushrooms:
        Mush.draw()
    update_canvas()
    delay(0.03)

# finalization code