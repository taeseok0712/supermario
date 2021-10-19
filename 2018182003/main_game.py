from pico2d import *
import random
from C_mario import mario
from C_state import state
from C_block import Block
from C_Stage1_Back_Ground import C_Stage1_Bk
import game_framework
import title_state
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

def collide_T_to_B(a,b):
    left_a, bottom_a, right_a, top_a = a.get_hitbox()
    left_b, bottom_b, right_b, top_b = b.get_hitbox()
    if bottom_a < top_b : return True

def handle_events():
    global running
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        if event.type == SDL_KEYDOWN and event.key == SDLK_RIGHT:
            player.state= state.S_move
            player.is_move = True
            player.dirction = 1
            player.move_dir = 1
        if event.type == SDL_KEYDOWN and event.key == SDLK_LEFT:
            player.state= state.S_move
            player.is_move = True
            player.dirction = 2
            player.move_dir = -1
        if event.type == SDL_KEYUP and event.key == SDLK_RIGHT:
            player.state = state.S_idle
            player.is_move = False
        if event.type == SDL_KEYUP and event.key == SDLK_LEFT:
            player.is_move = False
            player.state = state.S_idle
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
    global random_b
    global stage1_Bk
    global Platform
    global block
    global blocks
    global Grounds
    player = mario()
    stage1_Bk = C_Stage1_Bk()
    random_b=Block('random',200,200)
    platform_list=['random',900,300,'random',1500,300]

    Platform =[Block('random',20,30),Block('brick',500,200)]
    Grounds =[Ground(1104)]



def exit():
    global player , random_b ,stage1_Bk
    del (player)
    del (random_b)
    del (stage1_Bk)
def update():

    for block in Platform:
        block.update(player.scroll_x)
    for ground in Grounds:
        ground.update(player.scroll_x)
    player.update()
    random_b.update(player.scroll_x)
    stage1_Bk.update(player.scroll_x)




    if collide(player,random_b):
        player.is_Coll = True
        print(player.Coll_y)
        player.Coll_y = random_b.y + random_b.size_y/2
        if (collide_T_to_B(player, random_b)):
            random_b.is_hit = True
            random_b.is_coll = True
            player.Drop = True

    else:
        player.Drop = False



    for ground in Grounds:
        if collide(player, ground):
            player.is_Coll = True
            player.Coll_y = 80
        else:
            player.is_Coll = False




def draw():
    clear_canvas()
    stage1_Bk.draw()
    player.draw()
    for block in Platform:
        block.draw()
    for ground in Grounds:
        ground.draw()
    random_b.draw()
    update_canvas()
    delay(0.03)

# finalization code