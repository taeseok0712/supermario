import game_framework
from pico2d import *


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


GRAVITY = -9.8 * PIXEL_PER_METER
# m/s^2
ACCEL = 0.5
MAX_ACCEL = 3
CHARGE_POWER = 100
MAX_CHARGE = 50 * PIXEL_PER_METER
JUMP_POWER = 8 * PIXEL_PER_METER
# Boy Event
RIGHT_DOWN, LEFT_DOWN, RIGHT_UP, LEFT_UP, SHIFT_UP,SHIFT_DOWN, SPACE , COLL_B , COLL_U ,FALL,LANDING,LANDING_MOVE= range(12)

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
print(type(game_framework.frame_time))


class IdleState:

    def enter(mario, event):
        if event == RIGHT_DOWN:
            mario.velocity += RUN_SPEED_PPS
        elif event == LEFT_DOWN:
            mario.velocity -= RUN_SPEED_PPS
        elif event == RIGHT_UP:
            mario.velocity -= RUN_SPEED_PPS
        elif event == LEFT_UP:
            mario.velocity += RUN_SPEED_PPS

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

        mario.accel = mario.dir * ACCEL


        print('O')
    def do(mario):
        #boy.frame = (boy.frame + 1) % 8

        mario.move()

        if(mario.frame < 1):
            mario.frame = 1
        mario.frame = (mario.frame + mario.FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 4

        #print( game_framework.frame_time)



    def draw(mario):
        if mario.dir == 1:
            mario.image.clip_draw(32 * int(mario.frame), 32, mario.sizeX, mario.sizeY, mario.x, mario.y)
        else:
            mario.image.clip_draw(32 * int(mario.frame), 0, mario.sizeX, mario.sizeY, mario.x,mario.y)

class JumpState():

    def enter(mario, event):
        print("jumpenter")
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
        if not mario.jumpOn:
            mario.privY = mario.y
            mario.jumpOn = True
            mario.jumpTime = 0

        if event == SHIFT_DOWN:
            mario.jumpCharge = True
        if event == SHIFT_UP:
            mario.jumpCharge = False


        mario.frame = 4
        mario.dir = clamp(-1, mario.velocity, 1)

    def exit(mario, event):

        if mario.jumpOn == False:
            mario.jumpPower = JUMP_POWER
            mario.jumpTime = 0

    def do(mario):
        mario.move()
        mario.jumpTime += game_framework.frame_time
        if mario.jumpCharge:
            if mario.jumpPower < MAX_CHARGE:
                mario.jumpPower += CHARGE_POWER* game_framework.frame_time
        mario.y += (mario.jumpPower + GRAVITY * mario.jumpTime * 0.5)*game_framework.frame_time

        if mario.jumpPower + GRAVITY * mario.jumpTime <= 0:
            mario.privY = mario.y
            mario.add_event(FALL)
            mario.jumpOn = False






    def draw(mario):
        if mario.dir == 1:
            mario.image.clip_draw(32 * int(mario.frame), 32, mario.sizeX, mario.sizeY, mario.x, mario.y)
        else:
            mario.image.clip_draw(32 * int(mario.frame), 0, mario.sizeX, mario.sizeY, mario.x,mario.y)

class FallState():

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

        mario.frame = 4

    def exit(mario, event):
        mario.fallOn = False
        mario.jumpPower = JUMP_POWER



    def do(mario):
        mario.move()

        mario.jumpTime += game_framework.frame_time
        mario.y += GRAVITY * mario.jumpTime * 0.5 * game_framework.frame_time
        if(mario.y < 64):
            mario.y = 64
            if(mario.velocity == 0 ):
                mario.add_event(LANDING)
            else:
                mario.add_event(LANDING_MOVE)
            mario.jumpTime = 0


    def draw(mario):
        if mario.dir == 1:
            mario.image.clip_draw(32 * int(mario.frame), 32, mario.sizeX, mario.sizeY, mario.x, mario.y)
        else:
            mario.image.clip_draw(32 * int(mario.frame), 0, mario.sizeX, mario.sizeY, mario.x,mario.y)







next_state_table = {
    IdleState: {RIGHT_UP: RunState, LEFT_UP: RunState, RIGHT_DOWN: RunState, LEFT_DOWN: RunState, SPACE: IdleState , SHIFT_DOWN:JumpState,SHIFT_UP:IdleState},
    RunState: {RIGHT_UP: IdleState, LEFT_UP: IdleState, LEFT_DOWN: IdleState, RIGHT_DOWN: IdleState, SPACE: RunState,SHIFT_DOWN:JumpState,SHIFT_UP:RunState},
    JumpState:{RIGHT_UP: JumpState, LEFT_UP: JumpState, LEFT_DOWN: JumpState, RIGHT_DOWN: JumpState,SHIFT_DOWN:JumpState,SHIFT_UP:JumpState , FALL:FallState},
    FallState: {RIGHT_UP: FallState, LEFT_UP: FallState, LEFT_DOWN: FallState, RIGHT_DOWN: FallState, SHIFT_DOWN: FallState, SHIFT_UP: FallState ,LANDING:IdleState,LANDING_MOVE:RunState}
}

class Mario:

    def __init__(self):
        self.x, self.y = 1600 // 2, 64
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
        self.charge = CHARGE_POWER
        self.jumpOn = False
        self.fallOn = False
        self.jumpCharge = False
        self.jumpPower = JUMP_POWER
        self.jumpTime = 0
        self.jumpAccel = 0.2
        self.privY = self.y
    def get_bb(self):
        return self.x - (self.sizeX/2),self.y - (self.sizeY/2), self.x + (self.sizeX/2),self.y + (self.sizeY/2)


    def fire_ball(self):

        pass

    def move(self):
        if (self.accel > -MAX_ACCEL and self.accel< MAX_ACCEL):
            self.accel += self.accel *game_framework.frame_time

        self.x += self.velocity * game_framework.frame_time + self.accel
        self.x = clamp(25, self.x, 1600 - 25)
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
        debug_print(' vel' + str(self.velocity) )
        draw_rectangle(*self.get_bb())


    def handle_event(self, event):
        if (event.type, event.key) in key_event_table:
            key_event = key_event_table[(event.type, event.key)]
            self.add_event(key_event)

