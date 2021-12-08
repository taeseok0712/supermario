import game_framework
import pico2d
import start_state
import title_state
import edit_state
import main_state
import stage2
import stage3
x= 800
y = 600

pico2d.open_canvas(x,y)

game_framework.run(start_state)

pico2d.close_canvas()
