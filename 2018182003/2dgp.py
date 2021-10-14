from pico2d import *
import random
from C_mario import mario
from C_state import state
from C_Stage1_Back_Ground import C_Stage1_Bk

def handle_events():
    global running
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            running = False
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
        if event.type == SDL_KEYUP and event.key == SDLK_c:
            player.jump_charge = False

# initialization code
x = 1
open_canvas(1600,600)
player = mario()
stage1_Bk = C_Stage1_Bk()
running = True


# game main loop code
while running:

    handle_events()


    clear_canvas()
   #rander
    stage1_Bk.draw()
    player.draw()
    player.update()
    stage1_Bk.update(player.scroll_x)
    update_canvas()
    delay(0.03)

# finalization code