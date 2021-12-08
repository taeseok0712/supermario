from pico2d import *
import time
import server
TIME_LIMIT = 150


class C_UI_():

    def __init__(self):
        self.UI_image = load_image(('UI.png'))
        self.coin = 0
        self.life = 0
        self. stage = 0
        self.font = load_font('ENCR10B.TTF', 32)
        self.frame = 0
        self.Flame_Change_Start = time.time();
        self.Flame_Change_End = time.time();
        self.coin_image = load_image('UI_coin.png')
        self.time = 150
        self.t1 = time.time();
        self.t2 = time.time();
        self.timer = 0
        self.coin = 0
        self.stage = 1
    def draw(self):


        self.UI_image.draw(400, 300, 800, 600)
        self.font.draw(665 , 520,str(self.time), (255, 255, 255))

        self.font.draw(295, 525, str(server.score), (255, 255, 255))
        self.font.draw(465, 520, str(server.stage), (255, 255, 255))
        self.font.draw(510, 520, str(self.stage), (255, 255, 255))
        #draw_rectangle(255,530,271,514)
        # draw_rectangle(0,0,800 -self.scroll_x,80)

        self.coin_image.clip_draw(8*self.frame, 0, 8, 8, 260, 525 ,16 ,16)
    def update(self):

        self.Flame_Change_End = time.time();
        self.t2 = time.time()
        if self.t2 - self.t1 > 1:
            self.timer+=1
            self.t1 = time.time();

        self.time = TIME_LIMIT - int(self.timer)

        if self.Flame_Change_End - self.Flame_Change_Start > 0.1:
            self.frame = (self.frame + 1) % 3
            self.Flame_Change_Start = time.time();
        pass