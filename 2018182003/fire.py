from pico2d import *
import game_world
import game_framework
import server

PIXEL_PER_METER = (10.0 / 0.3)  # 10 pixel 30 cm
RUN_SPEED_KMPH = 40.0  # Km / Hour
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
FRAMES_PER_ACTION = 4
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)


TIME_PER_ACTION = 0.3
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FAllING_POWER =10

GRAVITY = -9.8 * PIXEL_PER_METER
# m/s^2
ACCEL = 0.5
MAX_ACCEL = 3

class Fire:
    image = None

    def __init__(self, x = 400, y = 200, dir = 1):
        if Fire.image == None:
            Fire.image = load_image('Fire.png')
        self.x, self.y, self.dir = x, y, dir
        self.frame = 0
        self.sizeX = 16
        self.sizeY = 16
    def get_bb(self):
        return self.x - (self.sizeX/2) ,self.y - (self.sizeY/2), self.x + (self.sizeX/2),self.y + (self.sizeY/2)

    def draw(self):
        self.image.clip_draw(16*int(self.frame), 0, 16, 16, self.x, self.y, 16, 16)

    def update(self):
        self.frame = (self.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % FRAMES_PER_ACTION
        self.x += RUN_SPEED_PPS * game_framework.frame_time * self.dir
        if self.x < 25 or self.x > 800 - 25:
            game_world.remove_object(self)
        for gumba in server.gumba:
            if collide(self,gumba):
                if not gumba.ishitted:
                    gumba.ishitted = True
                    game_world.remove_object(self)
            if gumba.dead:
                server.gumba.remove(gumba)
                game_world.remove_object(gumba)
        for turtle in server.turtle:
            if collide(self,turtle):
                if not turtle.ishitted:
                    turtle.dead = True
                    game_world.remove_object(self)

            if turtle.dead:
                server.turtle.remove(turtle)
                game_world.remove_object(turtle)

    def move(self):

        x1, y1 = self.x , self.y
        x2, y2 = self.x +64 , self.y +16
        x3, y3 = self.x + 128, self.y
        for i in range(0, 100, 2):
            t = i / 100
            x = (2 * t ** 2 - 3 * t + 1) * x1 + (-4 * t ** 2 + 4 * t) * x2 + (2 * t ** 2 - t) * x3
            y = (2 * t ** 2 - 3 * t + 1) * y1 + (-4 * t ** 2 + 4 * t) * y2 + (2 * t ** 2 - t) * y3

def collide(a, b):
    left_a, bottom_a, right_a, top_a = a.get_bb()
    left_b, bottom_b, right_b, top_b = b.get_bb()
    if left_a > right_b: return False
    if right_a < left_b: return False
    if top_a < bottom_b: return False
    if bottom_a > top_b: return False
    return True


