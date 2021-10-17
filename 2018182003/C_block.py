import pico2d
from pico2d import *
from C_state import state_block
import time
class Block:

    def __init__(self,type,x,y):
        self.type = type
        self.x = x
        self.y = y
        self.state = state_block.S_Idle
        self.is_coll = False
        self.is_hit = False
        self.frame = 0
        self.scroll_x = -500;
        self.type_a = -1
        self.Flame_Change_Start = time.time();
        self.Flame_Change_End = time.time();
        if self.type == 'random':
            self.type_a = 1
        if self.type == 'brick':
            self.type_a = 0
        self.image =load_image("Blocks.png")

    def draw(self):

        self.image.clip_draw(32*self.frame,32 * self.type_a ,32,32,self.x -self.scroll_x,self.y)

    def draw_1(self,w,h):
        self.image.clip_draw(32 * self.frame, 32 * self.type_a, 32, 32, self.x - self.scroll_x, self.y,w,h)

    def update(self,scroll_x):
        self.Flame_Change_End = time.time();


        self.scroll_x =scroll_x
        if(self.type_a == 1 and self.is_hit == False):
            if self.Flame_Change_End - self.Flame_Change_Start > 0.2:
                self.frame = (self.frame+1) % 2
                self.Flame_Change_Start = time.time();


