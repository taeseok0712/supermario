import game_framework
import main_state
from pico2d import *
import server
from ui import C_UI_
import game_world
import stage2
import stage3
import title_state


font = None
name = "Load"
image = None

bgm = None

timer = None

def enter():
    global image
    global timer
    global font
    global bgm
    if server.life > 0:
        image = load_image('load.png')
    else: image = load_image('gameover.png')
    if server.Game_End:
        image = load_image('ending.png')
    font = load_font('ENCR10B.TTF', 32)
    server.ui = C_UI_()
    timer = 1500
    if server.life <= 0:
        bgm = load_wav('smb_gameover.wav')
        bgm.set_volume(32)
        bgm.play()

    game_world.add_object(server.ui,0)

def exit():
    global image
    game_world.clear()
    server.clear()
    del (image)


def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        else:
            if (event.type, event.key) == (SDL_KEYDOWN, SDLK_ESCAPE):
                game_framework.quit()




def draw():
    clear_canvas()
    if server.life > 0:
        image.draw(400, 300,800,600 )
        for game_object in game_world.all_objects():
            game_object.draw()
        font.draw(425, 310, str(server.life), (255, 255, 255))
    else:
        image.draw(400, 300, 800, 600)
    if server.Game_End:
        image.draw(400, 300, 800, 600)
    update_canvas()







def update():
    global timer
    timer -= 1
    if timer < 0 and server.life > 0 and not server.Game_End:
        if server.stage == 1:
            game_framework.change_state(main_state)
        elif server.stage == 2:
            game_framework.change_state(stage2)
        elif server.stage == 3:
            game_framework.change_state(stage3)
    if timer < 0 and server.life <= 0:
        game_framework.change_state(title_state)
    if timer < 0 and server.Game_End:
        server.Game_End = False
        game_framework.change_state(title_state)






def pause():
    pass


def resume():
    pass






