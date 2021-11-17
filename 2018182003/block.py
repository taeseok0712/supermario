import game_framework
from pico2d import *

import time

import game_world
IDLE, HITTING, BROKING, BROKEN, HIT = range(5)

PIXEL_PER_METER = (10.0 / 0.3)  # 10 pixel 30 cm



TIME_PER_ACTION = 0.3
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION


GRAVITY = -9.8 * PIXEL_PER_METER
# m/s^2

#(mario.frame + mario.FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 4

# Boy States
print(type(game_framework.frame_time))

class Block:
    image = None

    def __init__(self, type = None,x= None,y= None):
        self.type = type
        self.x = x
        self.y = y
        self.size_x = 32
        self.size_y = 32
        self.state = IDLE
        self.is_coll = False
        self.is_hit = False
        self.frame = 0

        self.type_a = -1
        self.Flame_Change_Start = time.time();
        self.Flame_Change_End = time.time();
        self.move_on = False
        self.mario=None
        if self.type == 'random':
            self.type_a = 1
        if self.type == 'brick':
            self.type_a = 0
        if Block.image == None:
            Block.image =load_image("Blocks.png")

    def draw(self):
        self.image.clip_draw(32*self.frame,32 * self.type_a ,32,32,self.x,self.y)
        draw_rectangle(*self.get_bb())


    def get_bb(self):

        return self.x - (self.size_x/2),self.y - (self.size_y/2), self.x + (self.size_x/2),self.y + (self.size_y/2)

    def update(self):
        pass






