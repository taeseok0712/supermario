from pico2d import *

class C_UI_():

    def __init__(self):
        self.UI_image = load_image(('UI.png'))
        self.coin = 0
        self.life = 0
        self. stage = 0
    def draw(self):

        self.UI_image.draw(400, 300, 800, 600)

        # draw_rectangle(0,0,800 -self.scroll_x,80)

    def update(self, coin , Life , Stage):
        pass