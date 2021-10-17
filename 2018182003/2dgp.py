from pico2d import *
import random
from C_mario import mario
from C_state import state
from C_block import Block
from C_Stage1_Back_Ground import C_Stage1_Bk

def Coll_MB():
    global player
    global random_b

    m_size = 16
    b_size = 16
    coll =False
    if (player.x  - m_size < random_b.x + b_size - random_b.scroll_x and
            player.y - m_size  < random_b.y +b_size and
            player.x + m_size > random_b.x - random_b.scroll_x-b_size and
            player.y + m_size > random_b.y +-b_size
    ):
        print('c')
        player.is_Coll =True
        player.Coll_y = random_b.y

    else:
        player.is_Coll =False












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
        if event.type == SDL_KEYDOWN and event.key == SDLK_f:
            print(player.y)
            print(random_b.y)
        if event.type == SDL_KEYUP and event.key == SDLK_c:
            player.jump_charge = False

# initialization code
x = 1
open_canvas(800,600)
player = mario()
stage1_Bk = C_Stage1_Bk()
random_b=Block('random',500,200)
Brick_b=Block('brick',300,200)
platform_list=['random',900,300,'random',1500,300]


print(platform_list.count('random'))
running = True


# game main loop code
while running:

    handle_events()




    clear_canvas()
    #update
    player.update()
    Coll_MB()
    random_b.update(player.scroll_x)
    Brick_b.update(player.scroll_x)
    stage1_Bk.update(player.scroll_x)
   #rander
    stage1_Bk.draw()
    player.draw()
    random_b.draw()
    update_canvas()
    delay(0.03)

# finalization code