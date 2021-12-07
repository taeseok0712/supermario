import random

import game_framework
from pico2d import *
import server
import time
import game_world
from mushroom import MushRoom
from coin import Coin

IDLE, HITTING, BROKING, BROKEN, HIT = range(5)

PIXEL_PER_METER = (10.0 / 0.3)  # 10 pixel 30 cm



TIME_PER_ACTION = 0.3
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION


GRAVITY = -9.8 * PIXEL_PER_METER
# m/s^2


print(type(game_framework.frame_time))

class Block:
    image = None

    def __init__(self, type = None,x= None, y= None):
        self.type = type
        self.time = get_time()
        self.item = random.randint(0,3)
        self.x = x
        self.y = y
        self.size_x = 32
        self.size_y = 32
        self.state = IDLE
        self.is_coll = False
        self.is_hit = False
        self.frame = 0
        self.distance = 0
        self.type_a = -1
        self.Flame_Change_Start = time.time();
        self.Flame_Change_End = time.time();
        self.move_on = False

        self.add = False
        if self.type == 'random':
            self.type_a = 1
        if self.type == 'brick':
            self.type_a = 0
        if self.type == 'pipe_LB':
            self.type_a = 2
        if self.type == 'pipe_LU':
            self.type_a = 3
        if self.type == 'pipe_RB':
            self.type_a = 4
        if self.type == 'pipe_RU':
            self.type_a = 5

        if Block.image == None:
            Block.image =load_image("Blocks.png")

    def draw(self):
        self.image.clip_draw(32*self.frame,32 * self.type_a ,32,32,self.x-server.mario.scrollX,self.y)


    def get_bb(self):

        return self.x - (self.size_x/2)-server.mario.scrollX,self.y - (self.size_y/2), self.x + (self.size_x/2)-server.mario.scrollX,self.y + (self.size_y/2)

    def update(self):

        self.Flame_Change_End = time.time();
        self.move()

        if (self.type_a == 1 and self.is_hit == False):
            if self.Flame_Change_End - self.Flame_Change_Start > 0.3:
                self.frame = (self.frame + 1) % 3
                self.Flame_Change_Start = time.time();
        if (self.type_a == 1 and self.is_hit == True and self.state == IDLE):
            self.frame = 3
            self.state = HITTING
            if self.item == 1:
                server.item.append(MushRoom(self.x, self.y + self.size_y))
            else:
                coin = Coin(self.x, self.y + self.size_y)

                server.coin.append(Coin(self.x, self.y + self.size_y))
                server.ui.coin += 1
            self.add = True
            self.move_on = True

        if (self.type_a == 0 and self.is_hit == True and self.state == IDLE):
            self.state = HITTING
            self.Flame_Change_Start = time.time();
            self.move_on = True

    def move(self):
        if (self.move_on == True and self.state == HITTING):
            self.y += 5
            print('hit')
            self.move_on = False
        if self.Flame_Change_End - self.Flame_Change_Start > 0.28 and self.move_on == False and self.state == HITTING:
            self.y -= 5
            self.state = BROKEN
            if self.add == True:
                if self.item == 1:
                    game_world.add_objects(server.item,0)
                else:
                    game_world.add_objects(server.coin,0)


                self.add = False
            if (self.type_a == 0):
                self.state = IDLE
                self.is_hit = False

    def setMove(self):
        self.move_on = True
        self.is_hit = True
    def get_y(self):
        print(self.y)







