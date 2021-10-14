from pico2d import *
from C_mario import mario
class C_Stage1_Bk:
    def __init__(self):
        self.image =load_image('stage1.png')
        self.scroll_x =0
    def draw(self):
     #   self.image.clip_draw( 0,0,800,600,400-self.scroll_x,300)
        self.image.clip_draw(0, 0, 800, 600, 400 - self.scroll_x, 300)

    def update(self,x):
        self.scroll_x = x