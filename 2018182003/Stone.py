import pico2d
from pico2d import *
import time
import game_framework
import server
import game_world
RIGHT_DOWN, LEFT_DOWN, RIGHT_UP, LEFT_UP, SHIFT_UP, SHIFT_DOWN, SPACE ,  FALL, LANDING, LANDING_MOVE, CHANGE, GROW_TIMER, DEAD= range(13)
PIXEL_PER_METER = (10.0 / 0.3)  # 10 pixel 30 cm
RUN_SPEED_KMPH = 10.0  # Km / Hour
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
FRAMES_PER_ACTION = 2
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)


TIME_PER_ACTION = 0.3
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FAllING_POWER =20
RISE_SPEED = 200
GRAVITY = -9.8 * PIXEL_PER_METER
# m/s^2
ACCEL = 0.5
MAX_ACCEL = 3

class Stone:

    def __init__(self,cx,cy):
        self.x = cx
        self.y = cy
        self.collcnt = 0
        self.size_x = 48
        self.size_y = 64
        self.vel = RUN_SPEED_PPS
        self.frame = 0
        self.ishitted = False
        self.dead = False
        self.attack = False
        self.rise = False
        self.Flame_Change_Start = time.time()
        self.Flame_Change_End = time.time()
        self.image = load_image("Stone.png")
        self.isColl = False
        self.collcnt = 0
        self.falltime = 0
        self.originY = self.y
        self.CollY = 0

    def draw(self):
            self.image.clip_draw(24*self.frame, 0, 24, 32, self.x - server.mario.scrollX, self.y, 48, 64)


    def get_bb(self):
            return self.x-server.mario.scrollX - (self.size_x/2),self.y - (self.size_y/2), self.x-server.mario.scrollX + (self.size_x/2),self.y + (self.size_y/2)

    def update(self):
        self.Flame_Change_End = time.time()

        self.find()
        self.Rise()
        if self.x - server.mario.scrollX < 800:
            self.drop()
        if collide(self, server.mario):
            server.mario.dmg = True
            if server.mario.mario != 0:
                server.mario.add_event(CHANGE)


    def drop(self):
        if self.attack:
            self.frame = 2

            if not self.isColl and self.attack:
                self.collCheak()
                self.falltime += game_framework.frame_time
                self.y += FAllING_POWER * GRAVITY * self.falltime * 0.5 * game_framework.frame_time
            if self.isColl and not self.rise:
                self.y = self.CollY
                self.rise = True

    def Rise(self):
        if self.rise:

            if self.y < self.originY:
                self.frame = 1
                self.y += RISE_SPEED *game_framework.frame_time
            if self.y >= self.originY and self.rise and self.attack:

                self.y = self.originY
                self.rise = False
                self.falltime = 0
                self.attack = False
                self.collCheak()

    def find(self):
        if self.x > server.mario.x + server.mario.scrollX:
            if server.mario.x + server.mario.scrollX - self.x > -50:
                self.frame = 1
                if not self.rise and not self.attack:
                    self.attack = True



    def collCheak(self):
        self.collcnt = 0
        for block in server.blocks:
            if collide(self, block):
                self.collcnt += 1
                self.CollY = block.y + block.size_y/2 + self.size_y/2
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



