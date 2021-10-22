import game_framework
import pico2d
import start_state
import title_state
import main_game
x= 800
y = 600

pico2d.open_canvas(800,600)

game_framework.run(main_game)

pico2d.close_canvas()
