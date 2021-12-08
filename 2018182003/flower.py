import pico2d
from pico2d import *
import server

class Flower:


    def __init__(self,x,y):
        self.x = x
        self.y = y
        self.size_x = 32
        self.size_y = 32
        self.is_coll = False
        self.frame = 0
        self.scroll_x = 0;
        self.move_on = False
        self.is_exist = False
        self.image =load_image("flower.png")


    def draw(self):
            self.image.clip_draw(0, 0, 16, 16, self.x - server.mario.scrollX, self.y, 32, 32)

            draw_rectangle(*self.get_bb())

    def get_bb(self):
            return self.x-server.mario.scrollX - (self.size_x/2),self.y - (self.size_y/2), self.x-server.mario.scrollX + (self.size_x/2),self.y + (self.size_y/2)

    def update(self):
        pass