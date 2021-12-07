import pico2d
from pico2d import *
import time
import game_framework
import server

PIXEL_PER_METER = (10.0 / 0.3)  # 10 pixel 30 cm
RUN_SPEED_KMPH = 10.0  # Km / Hour
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
FRAMES_PER_ACTION = 2
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)


TIME_PER_ACTION = 0.3
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FAllING_POWER =10

GRAVITY = -9.8 * PIXEL_PER_METER
# m/s^2
ACCEL = 0.5
MAX_ACCEL = 3
BLOCK_SIZE=32
class Turtle:

    def __init__(self,cx,cy):
        self.x = cx
        self.y = cy + BLOCK_SIZE / 2
        self.collcnt = 0
        self.canKick = False
        self.size_x = 32
        self.size_y = 48
        self.shooton = False
        self.dir = -1
        self.maxX = self.x + 100
        self.minX = self.x - 100
        self.vel = RUN_SPEED_PPS
        self.frame = 0
        self.ishitted = False
        self.dead = False
        self.distance = 100
        self.Flame_Change_Start = time.time()
        self.Flame_Change_End = time.time()
        self.image = load_image("turtle.png")

    def draw(self):
            if self.dir == 1:
                self.image.clip_draw(16*int(self.frame), 0, 16, 24, self.x - server.mario.scrollX, self.y, self.size_x, self.size_y)
            if self.dir == -1:
                self.image.clip_draw(16*int(self.frame), 24, 16, 24, self.x - server.mario.scrollX, self.y, self.size_x, self.size_y)

            draw_rectangle(*self.get_bb())

    def get_bb(self):
            return self.x-server.mario.scrollX - (self.size_x/2),self.y - (self.size_y/2), self.x-server.mario.scrollX + (self.size_x/2),self.y + (self.size_y/2)

    def update(self):
        self.Flame_Change_End = time.time()
        if self.ishitted== False:


            self.frame = (self.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % FRAMES_PER_ACTION

            if self.x - server.mario.scrollX < 800 and not self.shooton:
                self.move()

        if self.ishitted and not self.canKick:
            self.frame = 2
            self.size_y = 32
            self.y -= 16
            self.canKick = True
        if self.shooton:
            self.shoot()

    def move(self):
        self.gravity()
        if not self.ishitted:
            if self.collcnt <= 2:
                self.x += self.vel * game_framework.frame_time * self.dir
                if self.x > self.maxX or self.x < self.minX:
                    self.dir = self.dir * -1

        if self.collcnt > 2 :
            self.x -= 3 +self.dir
        if self.collcnt == 0:
            self.y -= self.vel * 2 * game_framework.frame_time
        if self.y < 0:
            self.dead = True



    def gravity(self):
        self.collcnt = 0
        for block in server.blocks:
            if collide(self, block):
                self.collcnt += 1
        if self.collcnt == 0:
            self.isColl = False
        else:
            self.isColl = True

    def shoot(self):
        self.gravity()
        print(self.collcnt)
        if self.collcnt <= 2:
            self.x += self.vel * game_framework.frame_time * self.dir * 5
        if self.collcnt >= 3:
            self.dead = True
        if self.collcnt == 0:
            self.y -= self.vel * 2 * game_framework.frame_time
        if self.y < 0:
            self.dead = True
        if (self.x - server.mario.scrollX > 800 or self.x - server.mario.scrollX < 0) and self.shooton:
            self.dead = True



def collide(a, b):
    left_a, bottom_a, right_a, top_a = a.get_bb()
    left_b, bottom_b, right_b, top_b = b.get_bb()
    if left_a > right_b: return False
    if right_a < left_b: return False
    if top_a < bottom_b: return False
    if bottom_a > top_b: return False
    return True



