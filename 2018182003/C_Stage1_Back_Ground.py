from pico2d import *
from C_mario import mario
class C_Stage1_Bk:
    def __init__(self):
        self.image =load_image('World 1-1_1.png')
        self.scroll_x =0
        self.p_image = load_image('plat_form_1.png')
    def draw(self):
     #   self.image.clip_draw( 0,0,800,600,400-self.scroll_x,300)
      #  self.image.clip_draw(0, 0, 3376 * 2 , 600, 3376 - self.scroll_x, 300)
        self.image.clip_draw(0, 0, 3376, 240, 4000, 300 , 8000 , 600)


    def update(self,x):
        self.scroll_x = x