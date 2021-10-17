from pico2d import *
from C_state import state

class mario():
    def __init__(self):
        self.x =200
        self.y= 96
        self.scroll_x = 0
        self.state = state.S_idle
        self.frame = 0
        self.platform=[]
        self.gravity = 9.8
        self.priv_height =self.y
        self.accel =0
        self.jump_accel =0
        self.is_move = False
        self.dirction = 1
        self.move_dir = 1 #1이면 오른쪽 -1ㅇ면 왼쪽
        self.jump_power = 8
        self.jump_on =False
        self.Falling = False
        self.jump_charge = False
        self.image = load_image('player_Mario.png')
        self.jump_height = 0
        self.is_Coll = False
        self.Coll_y = 0

    def draw(self):

        self.image.clip_draw(32*self.frame, 192-(32* self.dirction), 32, 32, self.x, self.y)

    def update(self):

        if (self.is_move==True and self.jump_on == False):
            self.state =state.S_move
        if (self.is_move == True and self.jump_on == True):
            self.state = state.S_jump
        if(self.is_move):
            if self.x < 650- self.move_dir * self.accel and self.x >= 50- self.move_dir * self.accel :
                self.x += self.move_dir * self.accel

            elif self.x >= 650- self.move_dir * self.accel:
                if(self.scroll_x <7150):
                    self.scroll_x += self.move_dir * self.accel
            if self.accel < 10.0:
                 self.accel += 1
            self.priv_state = state.S_move

        if(self.jump_on):
            if (self.jump_charge == True):
                self.jump_power += 0.6

            self.jump_accel += 0.2
            self.jump_height = self.jump_power * self.jump_accel - self.gravity * (self.jump_accel ** 2) * 0.5
            if(self.jump_power * self.jump_accel > self.gravity * (self.jump_accel ** 2) * 0.5):
                #점프중
                if (self.is_Coll):
                    self.Falling = True
                    self.y = self.Coll_y -32 -self.jump_height
                self.y += self.jump_height
            if(self.jump_power * self.jump_accel < self.gravity * (self.jump_accel ** 2) * 0.5):
                #낙하중
                if (self.is_Coll):
                    self.Falling = False
                    self.jump_on = False
                    self.state = state.S_landing
                    self.y = self.Coll_y + 32 +0.5 * self.gravity * self.jump_accel
                self.y -= 0.5 * self.gravity * self.jump_accel

            if (self.y <= self.priv_height):
                self.jump_on=False
                self.y = self.priv_height
                self.state = state.S_landing

        if (self.Falling == True):
            self.jump_accel += 0.2
            self.y -= 0.5 * self.gravity * self.jump_accel
            if (self.y < self.priv_height):
                self.y = self.priv_height
                self.state = state.S_landing
                self.jump_on = False
                self.Falling = False

        if(self.jump_on ==False and self.Falling == False):
            self.jump_accel = 0
            self.jump_height = 0
            self.jump_power = 10



        if(self.state==state.S_move):
            self.frame = 1+(self.frame + 1) % 3

        if(self.state==state.S_idle):
            self.frame = 0
            self.accel = 0
        if (self.state == state.S_landing):
            self.frame = 0
        if (self.state == state.S_jump):
            self.frame = 4

