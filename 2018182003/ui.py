from pico2d import *
import time
class C_UI_():

    def __init__(self):
        self.UI_image = load_image(('UI.png'))
        self.coin = 0
        self.life = 0
        self. stage = 0
        self.font = load_font('ENCR10B.TTF', 16)
        self.frame = 0
        self.Flame_Change_Start = time.time();
        self.Flame_Change_End = time.time();
        self.coin_image = load_image('UI_coin.png')
        self.time = get_time()
        self.coin = 0
        self.stage = 1
    def draw(self):
        self.time = 150 -int(get_time())

        self.UI_image.draw(400, 300, 800, 600)
        self.font.draw(675 , 520,str(self.time), (255, 255, 255))

        self.font.draw(295, 525, str(self.coin), (255, 255, 255))
        self.font.draw(470, 520, str(1), (255, 255, 255))
        self.font.draw(515, 520, str(self.stage), (255, 255, 255))
        #draw_rectangle(255,530,271,514)
        # draw_rectangle(0,0,800 -self.scroll_x,80)

        self.coin_image.clip_draw(8*self.frame, 0, 8, 8, 260, 525 ,16 ,16)
    def update(self):
        self.Flame_Change_End = time.time();
        if self.Flame_Change_End - self.Flame_Change_Start > 0.1:
            self.frame = (self.frame + 1) % 3
            self.Flame_Change_Start = time.time();
        pass