from pico2d import *
from enum import Enum
open_canvas()
mario = load_image('player_Mario.png')



state = 1

running = True
x = 100
y =90
frame = 0
gravity = 9.8
dirc = 0
accel = 0
jump_accel =0
flame = 0
is_move = False
dirction = 1
priv = 0
state = 0 # 0:idle 1:move 2:jump
def handle_events():
    global running
    global priv
    global x
    global dirc
    global state
    global is_move
    global dirction
    global jump_accel
    events = get_events()
    for events in events:
        if events.type == SDL_QUIT:
            running = False
        if events.type == SDL_KEYDOWN and events.key == SDLK_ESCAPE:
            running = False
        if events.type == SDL_KEYDOWN and events.key == SDLK_RIGHT:
            dirc += 1
            state = 1
            is_move = True
            dirction = 1
        if events.type == SDL_KEYDOWN and events.key == SDLK_LEFT:
            dirc -= 1
            state = 1
            is_move = True
            dirction = 2
        if events.type == SDL_KEYUP and state != 2:
            dirc = 0
            state = 0
            is_move = False
        if events.type == SDL_KEYDOWN and events.key == SDLK_c:
            state = 2
            priv = y



    pass


while x < 800 and running:

    clear_canvas()

    mario.clip_draw(32*flame, 192-(32*dirction), 32, 32, x, 32+y)
    update_canvas()

    if state == 1:
        flame = 1+((flame +1)%3)

    if state == 0:
        flame = 0
    if state == 2:
        flame = 4
        jump_accel += 0.2
        higth =10 * jump_accel - gravity * jump_accel * jump_accel * 0.5
        y += higth
        if y <= priv:
            y=priv
            jump_accel=0
            state = 0




    if is_move :
        x += dirc * accel
        if accel < 4.0:
            accel += 0.05
    if is_move == False:
        accel = 0




    handle_events()


    delay(0.01)

close_canvas()

