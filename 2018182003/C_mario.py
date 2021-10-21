from pico2d import *
from C_state import *
import time
class mario():
    def __init__(self):
        self.M_State = Mario_state.mario

        self.x =200
        self.y= 96
        self.scroll_x = 0
        self.state = state.S_idle
        self.frame = 0
        self.gravity = 9.8
        self.priv_height =self.y
        self.accel =0
        self.jump_accel =0
        self.is_move = False
        self.dirction = 1
        self.move_dir = 1 #1이면 오른쪽 -1ㅇ면 왼쪽
        self.jump_power = 10
        self.jump_on =False
        self.Flame_Change_Start = time.time();
        self.Flame_Change_End = time.time();
        self.jump_charge = False
        self.image = load_image('player_Mario.png')
        self.image_G = load_image('Mario_grow.png')
        self.image_S = load_image('Super_mario.png')
        self.jump_height = 0
        self.is_Coll = False
        self.Coll_y = 0
        self.size_x = 32
        self.size_y = 32
        self.move_R = 0
        self.move_L = 0
        self.is_land = True
        self.First_frame = True
        self.M_state =Mario_state.mario
        self.Drop = False
        self.time_cnt = 0


    def get_hitbox(self):
        return self.x - (self.size_x/2),self.y - (self.size_y/2), self.x + (self.size_x/2),self.y + (self.size_y/2)


    def draw(self):

        if(self.M_state == Mario_state.mario):
            self.image.clip_draw(32*self.frame, 64-(32* self.dirction), self.size_x, self.size_y, self.x, self.y)
        if (self.M_state == Mario_state.Growing or self.M_state == Mario_state.Size_Dowm ):
            self.image_G.clip_draw(32 * self.frame, 128 - (64 *self.dirction), self.size_x, self.size_y, self.x, self.y)
        if (self.M_state == Mario_state.mario):
            self.image.clip_draw(32 * self.frame, 64 - (32 * self.dirction), self.size_x, self.size_y, self.x, self.y)
        if (self.M_state == Mario_state.Super_mario):
            self.image_S.clip_draw(32 * self.frame, 128 - (64 * self.dirction), self.size_x, self.size_y, self.x,self.y)
        draw_rectangle(*self.get_hitbox())


    def update(self):
        self.move_dir = self.move_R +self.move_L
        self.update_state()
        self.move()
        self.jump()
        if(self.M_state ==Mario_state.mario):
            self.size_y =32
        else:self.size_y = 64


    def move(self):

            if(self.move_dir == -1):
                self.dirction =2
            if(self.move_dir ==1):
                self.dirction =1

            if(self.move_dir == 0):
                self.is_move =False
                if(self.state != state.S_jump):
                    self.state = state.S_idle
            else:
                self.is_move =True

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
        self.Flame_Change_End =time.time()
        if self.is_move and self.jump_on == False:
            self.state = state.S_move
        if self.is_move and self.jump_on == True:
            self.state = state.S_jump
        if(self.M_state != Mario_state.Growing):
            if self.state == state.S_move:
                self.frame = 1 + (self.frame + 1) % 3
            if self.state == state.S_idle:
                self.frame = 0
                self.accel = 0
            if self.state == state.S_landing:
                self.frame = 0
            if self.state == state.S_jump:
                self.frame = 4
        if(self.M_state == Mario_state.Growing):
            if self.Flame_Change_End - self.Flame_Change_Start > 0.1:
                self.frame = (self.frame + 1) % 4
                self.time_cnt +=1

                self.Flame_Change_Start = time.time();
            if self.time_cnt == 8:
                self.M_state =Mario_state.Super_mario
                self.time_cnt = 0


        if (self.M_state == Mario_state.Size_Dowm):
            if self.Flame_Change_End - self.Flame_Change_Start > 0.1:
                self.frame = (self.frame + 1) % 4
                self.time_cnt += 1

                self.Flame_Change_Start = time.time();
            if self.time_cnt == 8:
                self.M_state = Mario_state.mario
                self.time_cnt = 0
                self.y -= 16


    def jump(self):

        if self.jump_on:

            self.jump_accel += 0.2
            vel = self.jump_power * self.jump_accel - self.gravity * (self.jump_accel ** 2) * 0.5
            print(vel)
            if self.jump_charge:
                self.jump_power += 0.6
            if (vel < 0): self.Drop = True;

            self.y += vel

            if (self.is_Coll and self.Drop):
                self.y = self.Coll_y + self.size_y / 2
                self.jump_on = False
                self.Drop = False


                self.jump_accel = 0
                self.jump_power = 10
                self.state = state.S_idle
        if self.Drop and self.jump_on == False:

            self.jump_accel += 0.05

            if (self.y - 5 * self.gravity * self.jump_accel * 0.5 < self.Coll_y):
                self.y = self.Coll_y + self.size_y / 2
                self.jump_on = False
                self.Drop = False

                self.jump_accel = 0
                self.jump_power = 10
                self.state = state.S_idle
            self.y -= 5 * self.gravity * self.jump_accel * 0.5













