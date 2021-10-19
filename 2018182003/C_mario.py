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
        self.jump_power = 10
        self.jump_on =False

        self.jump_charge = False
        self.image = load_image('player_Mario.png')
        self.jump_height = 0
        self.is_Coll = False
        self.Coll_y = 0
        self.size_x = 32
        self.size_y = 32
        self.First_frame = True
        self.Drop = False


    def get_hitbox(self):
        return self.x - (self.size_x/2),self.y - (self.size_y/2), self.x + (self.size_x/2),self.y + (self.size_y/2)
    def draw(self):

        self.image.clip_draw(32*self.frame, 192-(32* self.dirction), self.size_x, self.size_y, self.x, self.y)

        draw_rectangle(*self.get_hitbox())


    def update(self):
        self.update_state()
        self.move()
        self.jump()
        print(self.is_Coll)

    def move(self):

            if (self.is_move):
                if self.x < 650 - self.move_dir * self.accel and self.x >= 50 - self.move_dir * self.accel:
                    self.x += self.move_dir * self.accel

                elif self.x >= 650 - self.move_dir * self.accel:
                    if (self.scroll_x < 7150):
                        self.scroll_x += self.move_dir * self.accel
                if self.accel < 10.0:
                    self.accel += 0.5
                self.priv_state = state.S_move


    def update_state(self):
        if (self.is_move == True and self.jump_on == False):
            self.state = state.S_move
        if (self.is_move == True and self.jump_on == True):
            self.state = state.S_jump
        if (self.state == state.S_move):
            self.frame = 1 + (self.frame + 1) % 3

        if (self.state == state.S_idle):
            self.frame = 0
            self.accel = 0
        if (self.state == state.S_landing):
            self.frame = 0
        if (self.state == state.S_jump):
            self.frame = 4
    def jump(self):

        if (self.jump_on):
            vel = self.jump_power * self.jump_accel - self.gravity * (self.jump_accel ** 2) * 0.5
            self.jump_accel += 0.2
            if (self.jump_charge == True):
                self.jump_power += 0.6

            if self.jump_power * self.jump_accel >= self.gravity * (self.jump_accel ** 2) * 0.5 and self.Drop == False:
                self.y += vel
                if(self.First_frame):
                    self.First_frame = False
                elif(self.is_Coll): self.Drop = True
            if self.jump_power * self.jump_accel < self.gravity * (self.jump_accel ** 2) * 0.5 or self.Drop == True:
                self.y += vel

              
                if(self.is_Coll==True):

                    self.Drop= False


            if(self.is_Coll and self.Drop == True):
                self.jump_on = False
                self.Drop = False
                self.y = self.Coll_y + self.size_y/2
                self.jump_accel = 0
                self.jump_power = 10
                self.state = state.S_idle











