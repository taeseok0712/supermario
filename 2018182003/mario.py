import game_framework
from pico2d import *

import time

import game_world

# Boy Run Speed
PIXEL_PER_METER = (10.0 / 0.3)  # 10 pixel 30 cm
RUN_SPEED_KMPH = 20.0  # Km / Hour
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

# Boy Action Speed
TIME_PER_ACTION = 0.3
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION


GRAVITY = 9.8
ACCEL = 0.5
MAX_ACCEL = 3
# Boy Event
RIGHT_DOWN, LEFT_DOWN, RIGHT_UP, LEFT_UP, SHIFT_UP,SHIFT_DOWN, SPACE , COLL_B , COLL_U = range(9)

key_event_table = {
    (SDL_KEYDOWN, SDLK_RIGHT): RIGHT_DOWN,
    (SDL_KEYDOWN, SDLK_LEFT): LEFT_DOWN,
    (SDL_KEYDOWN, SDLK_LSHIFT): SHIFT_DOWN,
    (SDL_KEYUP, SDLK_RIGHT): RIGHT_UP,
    (SDL_KEYUP, SDLK_LEFT): LEFT_UP,
    (SDL_KEYUP, SDLK_LSHIFT): SHIFT_UP,
    (SDL_KEYDOWN, SDLK_SPACE): SPACE
}


# Boy States

class IdleState:

    def enter(mario, event):
        pass

    def exit(boy, event):
        if event == SPACE:
            boy.fire_ball()
        pass

    def do(mario):
        mario.frame = 0



    def draw(mario):
        if mario.dir == 1:
            mario.image.clip_draw(32 * int(mario.frame), 32, mario.sizeX, mario.sizeY, mario.x,mario.y)
        else:
            mario.image.clip_draw(32 * int(mario.frame), 0, mario.sizeX, mario.sizeY, mario.x,mario.y)

x = 0
class RunState:

    def enter(mario, event):
        if event == RIGHT_DOWN:
            mario.velocity += RUN_SPEED_PPS
        elif event == LEFT_DOWN:
            mario.velocity -= RUN_SPEED_PPS
        elif event == RIGHT_UP:
            mario.velocity -= RUN_SPEED_PPS
        elif event == LEFT_UP:
            mario.velocity += RUN_SPEED_PPS
        mario.dir = clamp(-1, mario.velocity, 1)
        mario.accel = mario.dir * ACCEL

    def exit(mario, event):
        if event == SPACE:
            mario.fire_ball()
        mario.velocity = 0
        mario.accel = mario.dir * ACCEL


        print('O')
    def do(mario):
        #boy.frame = (boy.frame + 1) % 8
        if (mario.accel > -MAX_ACCEL and mario.accel< MAX_ACCEL):
            mario.accel += mario.accel *game_framework.frame_time
        mario.velocity += mario.accel


        if(mario.frame < 1):
            mario.frame = 1
        mario.frame = (mario.frame + mario.FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 4
        #print( game_framework.frame_time)

        mario.x += mario.velocity * game_framework.frame_time

        mario.x = clamp(25, mario.x, 1600 - 25)

    def draw(mario):
        if mario.dir == 1:
            mario.image.clip_draw(32 * int(mario.frame), 32, mario.sizeX, mario.sizeY, mario.x, mario.y)
        else:
            mario.image.clip_draw(32 * int(mario.frame), 0, mario.sizeX, mario.sizeY, mario.x,mario.y)

class JumpState:

    def enter(mario, event):
        mario.frame = 5

        print("enter")
    def exit(mario, event):
        mario.jumpAccel = 0
        print("exit")

    def do(mario):
        mario.dir = clamp(-1, mario.velocity, 1)
        mario.jumpAccel += 30 * game_framework.frame_time
        mario.y += mario.jumpPower * mario.jumpAccel - GRAVITY * (mario.jumpAccel ** 2) * 0.5

        if(mario.y <96):
            mario.y = 96
            mario.add_event(COLL_B)


    def draw(mario):
        if mario.dir == 1:
            mario.image.clip_draw(32 * int(mario.frame), 32, mario.sizeX, mario.sizeY, mario.x, mario.y)
        else:
            mario.image.clip_draw(32 * int(mario.frame), 0, mario.sizeX, mario.sizeY, mario.x,mario.y)







next_state_table = {
    IdleState: {RIGHT_UP: RunState, LEFT_UP: RunState, RIGHT_DOWN: RunState, LEFT_DOWN: RunState, SPACE: IdleState , SHIFT_DOWN:JumpState,SHIFT_UP:JumpState},
    RunState: {RIGHT_UP: IdleState, LEFT_UP: IdleState, LEFT_DOWN: IdleState, RIGHT_DOWN: IdleState, SPACE: RunState,SHIFT_DOWN:JumpState,SHIFT_UP:JumpState},
    JumpState:{RIGHT_UP: IdleState, LEFT_UP: IdleState, LEFT_DOWN: IdleState, RIGHT_DOWN: IdleState,SHIFT_DOWN:JumpState,SHIFT_UP:JumpState , COLL_B:IdleState}
}

class Mario:

    def __init__(self):
        self.x, self.y = 1600 // 2, 96
        # Boy is only once created, so instance image loading is fine
        self.image = load_image('player_Mario.png')
        self.font = load_font('ENCR10B.TTF', 16)
        self.dir = 1
        self.velocity = 0
        self.frame = 0
        self.FRAMES_PER_ACTION = 3
        self.event_que = []
        self.cur_state = IdleState
        self.cur_state.enter(self, None)
        self.sizeX = 32
        self.sizeY = 32
        self.accel = ACCEL
        self.jumpPower = 10
        self.jumpAccel = 0.2
    def get_bb(self):
        return self.x - (self.sizeX/2),self.y - (self.sizeY/2), self.x + (self.sizeX/2),self.y + (self.sizeY/2)


    def fire_ball(self):

        pass


    def add_event(self, event):
        self.event_que.insert(0, event)

    def update(self):
        self.cur_state.do(self)
        if len(self.event_que) > 0:
            event = self.event_que.pop()
            self.cur_state.exit(self, event)
            self.cur_state = next_state_table[self.cur_state][event]
            self.cur_state.enter(self, event)

    def draw(self):
        self.cur_state.draw(self)
        #self.font.draw(self.x - 60, self.y + 50, '(Time: %3.2f)' % get_time(), (255, 255, 0))
        #fill here
        debug_print('Velocity :' + str(self.velocity) + '  Dir:' + str(self.dir) + ' State' + self.cur_state.__name__  + 'accel:' + str(self.accel))
        draw_rectangle(*self.get_bb())


    def handle_event(self, event):
        if (event.type, event.key) in key_event_table:
            key_event = key_event_table[(event.type, event.key)]
            self.add_event(key_event)

