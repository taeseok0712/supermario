import pico2d
from pico2d import *
import time

class cGumba:

    '''
    def __init__(self,x,y):
        self.x = x
        self.y = y
        self.size_x = 32
        self.size_y = 32
        self.speed
        self.frame = 0
        self.scroll_x = 0;
        self.image =load_image("mushroom.png")
    '''

    def __init__(self):
        self.x = 800
        self.y = 96
        self.size_x = 32
        self.size_y = 32

        self.frame = 0
        self.scroll_x = 0;
        self.ishitted = False
        self.dead = False
        self.Flame_Change_Start = time.time()
        self.Flame_Change_End = time.time()
        self.image = load_image("Gumba.png")

    def draw(self):
            self.image.clip_draw(16*self.frame, 0, 16, 16, self.x - self.scroll_x, self.y, 32, 32)

            draw_rectangle(*self.get_hitbox())

    def get_hitbox(self):
            return self.x-self.scroll_x - (self.size_x/2),self.y - (self.size_y/2), self.x-self.scroll_x + (self.size_x/2),self.y + (self.size_y/2)

    def update(self,scroll_x):
        speed = 5
        self.Flame_Change_End = time.time()

        if self.ishitted== False:
            if self.Flame_Change_End - self.Flame_Change_Start > 0.1:
                self.frame = (self.frame + 1) % 2
                self.Flame_Change_Start = time.time();
                self.x -=5
        if self.ishitted:

            self.frame = 2
            self.speed = 0
            if self.Flame_Change_End - self.Flame_Change_Start > 0.2:
                self.dead = True

        if(self.x - self.scroll_x < 0):
            self.dead = True
        self.scroll_x = scroll_x

    def get_dead(self):

        return self.dead

    def set_hitted(self):
        self.ishitted = True

    def get_hitted(self):
        return self.ishitted








