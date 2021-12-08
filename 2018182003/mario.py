import game_framework
from pico2d import *
import server

import random
import game_world



PIXEL_PER_METER = (10.0 / 0.3)  # 10 pixel 30 cm
RUN_SPEED_KMPH = 20.0  # Km / Hour
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)


TIME_PER_ACTION = 0.3
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FAllING_POWER =10

GRAVITY = -9.8 * PIXEL_PER_METER
# m/s^2
ACCEL = 0.5
MAX_ACCEL = 3
CHARGE_POWER = 100
MAX_CHARGE = 50 * PIXEL_PER_METER
JUMP_POWER = 8 * PIXEL_PER_METER
# Boy Event
RIGHT_DOWN, LEFT_DOWN, RIGHT_UP, LEFT_UP, SHIFT_UP, SHIFT_DOWN, SPACE , COLL_B , COLL_U , FALL, LANDING, LANDING_MOVE, CHANGE, GROW_TIMER, DEAD= range(15)
Idle, Jump , Land , Fall , Run= range(5)

MARIO,SUPER,FIRE = range(3)

eventName = ['RIGHT_DOWN', 'LEFT_DOWN', 'RIGHT_UP', 'LEFT_UP', 'SHIFT_UP','SHIFT_DOWN', 'SPACE' , 'COLL_B' , 'COLL_U' ,'FALL','LANDING','LANDING_MOVE']
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
        mario.state = Idle
        print(mario.collcnt)
        mario.gravity()
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
            mario.image.clip_draw(32 * int(mario.frame), mario.sizeY, mario.sizeX, mario.sizeY, mario.x,mario.y)
        else:
            mario.image.clip_draw(32 * int(mario.frame), 0, mario.sizeX, mario.sizeY, mario.x,mario.y)

x = 0
class RunState:

    def enter(mario, event):
        mario.state = Run
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
        mario.isColl = False

    def exit(mario, event):
        if event == SPACE:
            mario.fire_ball()

        mario.accel = mario.dir * ACCEL

    def do(mario):
        mario.move()

        if(mario.frame < 1):
            mario.frame = 1
        mario.frame = (mario.frame + mario.FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 4




    def draw(mario):
        if mario.dir == 1:
            mario.image.clip_draw(32 * int(mario.frame), mario.sizeY, mario.sizeX, mario.sizeY, mario.x, mario.y)
        else:
            mario.image.clip_draw(32 * int(mario.frame), 0, mario.sizeX, mario.sizeY, mario.x,mario.y)

class ChangeState:

    def enter(mario, event):
        if mario.change == False and mario.dmg == False and mario.mario == MARIO:
            mario.image = load_image('Mario_grow.png')
            mario.time = 100
            mario.sizeY = 64
            mario.y +=16
            mario.change = True

        if mario.change == False and mario.dmg == True and mario.mario == SUPER:

            mario.image = load_image('Mario_grow.png')
            mario.time = 100

            mario.change = True

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
        mario.isColl = False

    def exit(mario, event):
        if event == SPACE:
            mario.fire_ball()
        mario.accel = mario.dir * ACCEL



    def do(mario):
        mario.move()
        mario.time -= 1
        if mario.time == 0 and mario.dmg == False:
            mario.add_event(GROW_TIMER)
            mario.image = load_image('Super_mario.png')
            mario.mario = SUPER
            mario.change = False
        if mario.time == 0 and mario.dmg == True:
            mario.add_event(GROW_TIMER)
            mario.image = load_image('player_Mario.png')
            mario.dmg = False
            mario.sizeY = 32
            mario.y -= 16
            mario.mario = MARIO
            mario.change = False

        mario.frame = (mario.frame + mario.FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 4




    def draw(mario):
        if mario.dir == 1:
            mario.image.clip_draw(32 * int(mario.frame), mario.sizeY, mario.sizeX, mario.sizeY, mario.x, mario.y)
        else:
            mario.image.clip_draw(32 * int(mario.frame), 0, mario.sizeX, mario.sizeY, mario.x,mario.y)
class JumpState():

    def enter(mario, event):
        mario.state = Jump
        mario.onGround = False
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

        for block in server.blocks:
            if collide(mario, block):
                mario.jumpOn = False
                mario.setX()

                block.setMove()
                if mario.mario != MARIO and block.type =='brick':
                    server.blocks.remove(block)
                    game_world.remove_object(block)

                mario.add_event(FALL)




    def draw(mario):
        if mario.dir == 1:
            mario.image.clip_draw(32 * int(mario.frame), mario.sizeY, mario.sizeX, mario.sizeY, mario.x, mario.y)
        else:
            mario.image.clip_draw(32 * int(mario.frame), 0, mario.sizeX, mario.sizeY, mario.x,mario.y)

class FallState():

    def enter(mario, event):
        mario.state = Fall
        mario.onGround = False
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
        if not mario.catchMonster:
            mario.jumpTime += game_framework.frame_time
            mario.y += FAllING_POWER *GRAVITY * mario.jumpTime * 0.5 * game_framework.frame_time
            for block in server.blocks:
                if collide(mario, block):
                    if (mario.y < block.y):
                        mario.y = block.y+block.size_y/2 +mario.sizeY/2
                        if (mario.velocity == 0):
                            mario.add_event(LANDING)
                        else:
                            mario.add_event(LANDING_MOVE)
                        mario.jumpTime = 0
        else:
            if mario.y - mario.catchY < mario.distance:
                mario.y += 1
            else:
                mario.catchMonster = False

    def draw(mario):
        if mario.dir == 1:
            mario.image.clip_draw(32 * int(mario.frame), mario.sizeY, mario.sizeX, mario.sizeY, mario.x, mario.y)
        else:
            mario.image.clip_draw(32 * int(mario.frame), 0, mario.sizeX, mario.sizeY, mario.x,mario.y)
class DeadState():

    def enter(mario, event):
        mario.vel = 0
        mario.frame = 10

    def exit(mario, event):
        pass

    def do(mario):
        if mario.y - mario.hitY < 32 and not mario.fallOn:
            mario.y += 1
            if mario.y - mario.hitY == 32:
                mario.fallOn = True
        if mario.fallOn:
            mario.jumpTime += game_framework.frame_time
            mario.y += FAllING_POWER *GRAVITY * mario.jumpTime * 0.5 * game_framework.frame_time

    def draw(mario):
        if mario.dir == 1:
            mario.image.clip_draw(32 * int(mario.frame), mario.sizeY, mario.sizeX, mario.sizeY, mario.x, mario.y)
        else:
            mario.image.clip_draw(32 * int(mario.frame), 0, mario.sizeX, mario.sizeY, mario.x,mario.y)




next_state_table = {
    IdleState: {RIGHT_UP: RunState, LEFT_UP: RunState, RIGHT_DOWN: RunState, LEFT_DOWN: RunState, SPACE: IdleState , SHIFT_DOWN:JumpState, SHIFT_UP:IdleState, FALL:FallState, LANDING:IdleState, CHANGE:ChangeState,DEAD:DeadState},
    RunState: {RIGHT_UP: IdleState, LEFT_UP: IdleState, LEFT_DOWN: IdleState, RIGHT_DOWN: IdleState, SPACE: RunState, SHIFT_DOWN:JumpState, SHIFT_UP:RunState, LANDING_MOVE:RunState, FALL:FallState, LANDING:IdleState, CHANGE:ChangeState,DEAD:DeadState},
    JumpState:{RIGHT_UP: JumpState, LEFT_UP: JumpState, LEFT_DOWN: JumpState, RIGHT_DOWN: JumpState, SHIFT_DOWN:JumpState, SHIFT_UP:JumpState , FALL:FallState, CHANGE:ChangeState,DEAD:DeadState},
    FallState: {RIGHT_UP: FallState, LEFT_UP: FallState, LEFT_DOWN: FallState, RIGHT_DOWN: FallState, SHIFT_DOWN: FallState, SHIFT_UP: FallState , LANDING:IdleState, LANDING_MOVE:RunState, FALL:FallState, CHANGE:ChangeState,DEAD:DeadState},
    DeadState: {DEAD:DeadState},

    ChangeState: {RIGHT_UP: ChangeState, LEFT_UP: ChangeState, LEFT_DOWN: ChangeState, RIGHT_DOWN: ChangeState, SHIFT_DOWN: ChangeState, SHIFT_UP: ChangeState , LANDING:ChangeState, LANDING_MOVE:ChangeState, FALL:ChangeState, CHANGE:ChangeState, GROW_TIMER:IdleState,DEAD:DeadState}
}

class Mario:

    def __init__(self):
        self.x, self.y = 100, 64
        self.state = Idle
        self.distance = 32
        self.mario = MARIO #마리오의 상태 (작은,슈퍼,파이어)
        self.image = load_image('player_Mario.png')
        self.font = load_font('ENCR10B.TTF', 16)
        self.dir = 1
        self.collcnt = 0
        self.scrollX = 0
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
        self.isColl = False
        self.jumpCharge = False
        self.gameEnd = False
        self.jumpPower = JUMP_POWER
        self.jumpTime = 0
        self.jumpAccel = 0.2
        self.onGround = True
        self.change = False
        self.catchMonster = False
        self.dmg = False # 데미지 입었나 확인하는 변수
        self.time = 0
        self.dead = False
        self.catchY = self.y
        self.hitY = self.y
    def get_bb(self):
        return self.x - (self.sizeX/2) + 5,self.y - (self.sizeY/2), self.x - 5+ (self.sizeX/2),self.y + (self.sizeY/2)


    def fire_ball(self):

        pass

    def move(self):
        if (self.accel > -MAX_ACCEL and self.accel< MAX_ACCEL):
            self.accel += self.accel *game_framework.frame_time
        if self.collcnt <= 2:
            self.x += self.velocity * game_framework.frame_time + self.accel
        if self.collcnt > 2 and self.dir == 1:
            self.x -= 3
        if self.collcnt > 2 and self.dir == -1:
            self.x += 3
        self.x = clamp(25,self.x,650)
        if self.x == 650:
            if (self.scrollX + self.velocity * game_framework.frame_time + self.accel < 5950):
                self.scrollX += self.velocity * game_framework.frame_time + self.accel
        if self.x == 25:
            if(self.scrollX +self.velocity * game_framework.frame_time + self.accel  >0):
                self.scrollX += self.velocity * game_framework.frame_time + self.accel

    def add_event(self, event):
        self.event_que.insert(0, event)

    def update(self):

        self.cur_state.do(self)
        if len(self.event_que) > 0:
            event = self.event_que.pop()
            self.cur_state.exit(self, event)
            try:
                self.cur_state = next_state_table[self.cur_state][event]
            except:

                print("curState:", self.cur_state.__name__, "event:", eventName[event])
                exit(-1)
            self.cur_state.enter(self, event)
        if self.dir ==0:
            self.dir = 1

        self.gravity()
        if self.isColl == False and self.jumpOn == False and not self.dead:
            self.add_event(FALL)
        for item in server.item:
            if collide(self,item):
                server.item.remove(item)
                game_world.remove_object(item)
                if self.mario == MARIO:
                    self.add_event(CHANGE)

        for gumba in server.gumba:
            if collide(self,gumba):
                if self.state == Fall and not gumba.ishitted and not self.dead:
                    gumba.ishitted = True
                    self.catchY = self.y
                    self.catchMonster = True
                else:
                    if not gumba.ishitted:
                        if self.mario != MARIO:
                            self.dmg = True
                            self.add_event(CHANGE)
                        if self.mario == MARIO:
                            self.hitY = self.y
                            self.dmg = True
                            self.dead = True

            if gumba.dead:
                server.gumba.remove(gumba)
                game_world.remove_object(gumba)
        for turtle in server.turtle:
            if collide(self,turtle):
                if self.state == Fall and not turtle.ishitted and not self.dead:
                    turtle.ishitted = True
                    self.catchY = self.y
                    self.catchMonster = True
                if turtle.canKick and turtle.ishitted and not turtle.shooton:
                    turtle.dir = self.dir
                    turtle.shooton = True
                else:
                    if not turtle.ishitted and not turtle.canKick:
                        if self.mario != MARIO:
                            self.dmg = True
                            self.add_event(CHANGE)
                        if self.mario == MARIO:
                            self.hitY = self.y
                            self.dmg = True
                            self.dead = True

            if turtle.dead:
                server.turtle.remove(turtle)
                game_world.remove_object(turtle)

        if self.mario == MARIO and self.dmg:
            self.add_event(DEAD)


        if self.y < 0:
            self.gameEnd = True

    def draw(self):
        self.cur_state.draw(self)

        #fill here
        debug_print('x: ' + str(self.x+self.scrollX)+ 'y: ' + str(self.y) )



    def handle_event(self, event):
        if (event.type, event.key) in key_event_table and not self.dead:
            key_event = key_event_table[(event.type, event.key)]
            self.add_event(key_event)
        elif event.type == SDL_KEYDOWN and event.key == SDLK_g:
            if self.mario == MARIO:
                self.add_event(CHANGE)
            if self.mario == SUPER:
                self.dmg = True
                self.add_event(CHANGE)
    def setX(self):
        self.y -= 5

    def gravity(self):
        self.collcnt = 0
        for block in server.blocks:
            if collide(self, block):
                self.collcnt += 1
        if self.collcnt == 0:
            self.isColl = False
        else:

            self.isColl = True



def collide(a, b):
    left_a, bottom_a, right_a, top_a = a.get_bb()
    left_b, bottom_b, right_b, top_b = b.get_bb()
    if left_a > right_b: return False
    if right_a < left_b: return False
    if top_a < bottom_b: return False
    if bottom_a > top_b: return False
    return True
