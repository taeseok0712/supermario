import pico2d
from pico2d import *
import server
import game_framework

TIME_PER_ACTION = 0.3
ACTION_PER_TIME = 2.0 / TIME_PER_ACTION
COIN_SPEED = 150
class Coin:


    def __init__(self,x,y):
        self.x = x
        self.y = y
        self.size_x = 22
        self.size_y = 22
        self.FRAMES_PER_ACTION = 3
        self.is_coll = False
        self.frame = 0
        self.scroll_x = 0;
        self.move_on = False
        self.is_exist = False
        self.up = False
        self.remove = False
        self.originY = self.y
        self.coin_image = load_image('UI_coin.png')


    def draw(self):

            self.coin_image.clip_draw(8 * int(self.frame), 0, 8, 8, self.x - server.mario.scrollX, self.y, self.size_x,self.size_y)
            draw_rectangle(*self.get_hitbox())

    def get_hitbox(self):
            return self.x-server.mario.scrollX - (self.size_x/2),self.y - (self.size_y/2), self.x-server.mario.scrollX + (self.size_x/2),self.y + (self.size_y/2)

    def update(self):
        self.frame = (self.frame + self.FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 2

        if self.y - self.originY < 60:
            self.y += COIN_SPEED * game_framework.frame_time
        else: self.remove = True


