from pico2d import *

class Stage1BG:
    def __init__(self):
        self.image = load_image('World 1-1.png')
        self.scroll_x = 0


    def update(self):
        pass

    def draw(self):
        self.image.clip_draw(0, 0, 3376 * 2, 600, 3376 - self.scroll_x, 300)
        # fill here


