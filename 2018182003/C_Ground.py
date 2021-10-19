import pico2d
from pico2d import *


class Ground:


    def __init__(self,x):
        self.x = x
        self.size_x = 1104
        self.size_y = 32
        self.is_coll = False
        self.is_hit = False
        self.frame = 0
        self.scroll_x = -500;
        self.move_on = False
        self.image1 =load_image("Ground_1.png")


    def draw(self):

        self.image1.clip_draw(0 , 0 ,self.size_x , 32 , self.x -self.scroll_x , 40 ,  self.size_x*2,80)

        draw_rectangle(*self.get_hitbox())

    def get_hitbox(self):
        return self.x-self.scroll_x - (self.size_x),0, self.x-self.scroll_x + (self.size_x),80

    def update(self,scroll_x):
        self.scroll_x = scroll_x








