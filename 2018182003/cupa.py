import pico2d
from pico2d import *
import time
import game_framework
import server
import game_world
import math
PIXEL_PER_METER = (10.0 / 0.3)  # 10 pixel 30 cm
RIGHT_DOWN, LEFT_DOWN, RIGHT_UP, LEFT_UP, SHIFT_UP, SHIFT_DOWN, SPACE ,  FALL, LANDING, LANDING_MOVE, CHANGE, GROW_TIMER, DEAD= range(13)
RUN_SPEED_KMPH = 10.0  # Km / Hour
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
FRAMES_PER_ACTION = 4
FRAMES_PER_ACTION_FIRE = 2
FRAMES_PER_ACTION_HAMMER = 4
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)
HAMMERTIMER = 150
FIRETIMER = 200

TIME_PER_ACTION = 0.3
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FAllING_POWER =10

GRAVITY = -9.8 * PIXEL_PER_METER
# m/s^2
ACCEL = 0.5
MAX_ACCEL = 3
BLOCK_SIZE=32
class Cupa:

    def __init__(self,cx,cy):
        self.x = cx
        self.y = cy + BLOCK_SIZE/2
        self.collcnt = 0
        self.canKick = False
        self.size_x = 64
        self.size_y = 64
        self.shooton = False
        self.dir = -1
        self.maxX = self.x + 75
        self.minX = self.x - 75
        self.vel = RUN_SPEED_PPS
        self.frame = 0
        self.ishitted = False
        self.dead = False
        self.distance = 100
        self.firetimer = FIRETIMER
        self.hammertimer = HAMMERTIMER
        self.hammertime = 0
        self.hammercnt = 0
        self.falltime = 0
        self.Flame_Change_Start = time.time()
        self.Flame_Change_End = time.time()
        self.image = load_image("Cupa.png")

    def draw(self):

        self.image.clip_draw(32 * int(self.frame), 0, 32, 32, self.x - server.mario.scrollX, self.y, self.size_x, self.size_y)


    def get_bb(self):
            return self.x-server.mario.scrollX - (self.size_x/2),self.y - (self.size_y/2), self.x-server.mario.scrollX + (self.size_x/2),self.y + (self.size_y/2)

    def update(self):
        self.Flame_Change_End = time.time()
        if self.x - server.mario.scrollX < 800:
            self.firetimer -= 1
            self.hammertimer -= 1
            self.move()
            self.fire()
            self.hammer()
        if self.ishitted== False:
            self.frame = (self.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % FRAMES_PER_ACTION
        if collide(self, server.mario):
            server.mario.dmg = True
            if server.mario.mario != 0:
                server.mario.add_event(CHANGE)
        if self.y < 0:

            game_world.remove_object(self)
            server.cupa.remove(self)


    def move(self):
        self.gravity()

        if not self.ishitted:
            self.x += self.vel * game_framework.frame_time * self.dir

            if self.x > self.maxX or self.x < self.minX:
                self.dir = self.dir * -1
        if not self.isColl:
            self.falltime += game_framework.frame_time

            self.y += FAllING_POWER *GRAVITY * self.falltime * 0.5 * game_framework.frame_time


    def fire(self):
        if self.firetimer < 0 :
            fire_Cupa = Cupa_fire(self.x, self.y- 10, -1)
            game_world.add_object(fire_Cupa, 1)
            self.firetimer = FIRETIMER


    def hammer(self):
        if self.hammertimer < 0:
            hammer = Cupa_hammer(self.x, self.y, -1 , 70)
            game_world.add_object(hammer, 1)
            hammer2 = Cupa_hammer(self.x, self.y, -1, 30)
            game_world.add_object(hammer2, 1)
            self.hammertimer = HAMMERTIMER




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

class Cupa_fire:
    image = None

    def __init__(self, x = 400, y = 200, dir = 1):
        if Cupa_fire.image == None:
            Cupa_fire.image = load_image('cupa_fire.png')
        self.x, self.y, self.dir = x - 32, y+ 16, dir
        self.frame = 0
        self.sizeX = 48
        self.sizeY = 16
    def get_bb(self):
        return self.x - (self.sizeX/2)-server.mario.scrollX ,self.y - (self.sizeY/2), self.x + (self.sizeX/2)-server.mario.scrollX,self.y + (self.sizeY/2)

    def draw(self):
        self.image.clip_draw(48*int(self.frame), 0, 48, 16, self.x-server.mario.scrollX, self.y, 48, 16)


    def update(self):
        self.frame = (self.frame + FRAMES_PER_ACTION_FIRE * ACTION_PER_TIME * game_framework.frame_time) % FRAMES_PER_ACTION_FIRE
        self.x += RUN_SPEED_PPS * game_framework.frame_time * self.dir * 4
        if self.x -server.mario.scrollX < 25:
            game_world.remove_object(self)
        if collide(self, server.mario):
            game_world.remove_object(self)
            server.mario.dmg = True
            if server.mario.mario != 0:
                server.mario.add_event(CHANGE)



def collide(a, b):
    left_a, bottom_a, right_a, top_a = a.get_bb()
    left_b, bottom_b, right_b, top_b = b.get_bb()
    if left_a > right_b: return False
    if right_a < left_b: return False
    if top_a < bottom_b: return False
    if bottom_a > top_b: return False
    return True

class Cupa_hammer:

    image = None

    def __init__(self, x, y, dir = 1, mario_x = 0 , a = 70):
        if Cupa_hammer.image == None:
            Cupa_hammer.image = load_image('hammer.png')
        self.x, self.y, self.dir = x - 32, y+ 16, dir

        self.taget_x = mario_x
        self.frame = 0
        self.sizeX = 32
        self.sizeY = 32
        self.speed = 10
        self.angle = a * 3.141592 /180
        self.gravity = 100
        self.time = 0
        self.bounce = 0


    def get_bb(self):
        return self.x - (self.sizeX/2)-server.mario.scrollX ,self.y - (self.sizeY/2), self.x-server.mario.scrollX + (self.sizeX/2),self.y + (self.sizeY/2)

    def draw(self):
        self.image.clip_draw(16*int(self.frame), 0, 16, 16, self.x-server.mario.scrollX, self.y, self.sizeX, self.sizeY)


    def update(self):
        self.frame = (self.frame + FRAMES_PER_ACTION_HAMMER * ACTION_PER_TIME * game_framework.frame_time) % FRAMES_PER_ACTION_HAMMER
        self.x += RUN_SPEED_PPS * game_framework.frame_time * self.dir * 4
        self.move()
        if self.x-server.mario.scrollX < 25:
            game_world.remove_object(self)
        if collide(self, server.mario):
            game_world.remove_object(self)
            server.mario.dmg = True
            if server.mario.mario != 0:
                server.mario.add_event(CHANGE)



    def move(self):
        self.bounce = math.tan(self.angle) - (self.gravity/(2.0 * self.speed **2 * math.cos(self.angle)**2 )) * self.time**2
        self.time += game_framework.frame_time
        self. y = self. y + self.bounce


def collide(a, b):
    left_a, bottom_a, right_a, top_a = a.get_bb()
    left_b, bottom_b, right_b, top_b = b.get_bb()
    if left_a > right_b: return False
    if right_a < left_b: return False
    if top_a < bottom_b: return False
    if bottom_a > top_b: return False
    return True



