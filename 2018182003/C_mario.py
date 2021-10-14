from pico2d import *
from C_state import state

class mario():
    def __init__(self):
        self.x =100
        self.y= 15
        self.scroll_x = 0
        self.state = state.S_idle
        self.frame = 0
        self.gravity = 9.8
        self.priv_height =self.y
        self.accel =0
        self.jump_accel =0
        self.is_move = False
        self.priv_state = state.S_idle
        self.dirction = 1
        self.move_dir = 1 #1이면 오른쪽 -1ㅇ면 왼쪽
        self.jump_power = 8
        self.jump_on =False
        self.jump_charge = False
        self.image = load_image('player_Mario.png')
        self.jump_height = 0

    def draw(self):

        self.image.clip_draw(32*self.frame, 192-(32* self.dirction), 32, 32, self.x, 32+self.y)

    def update(self):
        if (self.is_move==True and self.jump_on == False):
            self.state =state.S_move
        if (self.is_move == True and self.jump_on == True):
            self.state = state.S_jump
        if(self.is_move):
            if self.x < 750- self.move_dir * self.accel:

                self.x += self.move_dir * self.accel

            elif self.x >= 750- self.move_dir * self.accel:
                print(self.scroll_x)
                self.scroll_x += self.move_dir * self.accel
            if self.accel < 10.0:
                 self.accel += 1
            self.priv_state = state.S_move

        if(self.jump_on):
            self.jump_accel += 0.2
            if (self.jump_charge == True):
                self.jump_power += 0.5
            print(self.jump_power)

            if (self.jump_accel == 0):
                self.priv_height = self.y
            self.jump_height = self.jump_power * self.jump_accel - self.gravity * (self.jump_accel ** 2) * 0.5
            self.y += self.jump_height

            if (self.y <= self.priv_height):
                self.y = self.priv_height
                self.jump_accel = 0
                self.jump_height = 0
                self.state = state.S_landing
                self.priv_state = state.S_landing
                self.jump_power = 10
                self.jump_on=False


        if(self.state==state.S_move):
            self.frame = 1+(self.frame + 1) % 3

        if(self.state==state.S_idle):
            self.frame = 0
            self.accel = 0
        if (self.state == state.S_landing):
            self.frame = 0
        if (self.state == state.S_jump):
            self.frame = 4


