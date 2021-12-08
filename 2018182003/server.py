MARIO,SUPER,FIRE = range(3)
state = MARIO
mario = None
score = 0
stage = None
blocks = []
item = []
ui = None
coin = []
gumba = []
turtle = []
flower = []
Flag = False
life = None
stone = []
cupa = []
Game_End = False
def clear():
    global mario
    global blocks
    global item
    global ui
    global coin
    global gumba
    global turtle
    global flower
    global Flag
    global cupa
    global Game_End
    global stone

    cupa = []
    blocks = []
    item = []
    ui = None
    stone = []
    coin = []
    gumba = []
    turtle = []
    flower = []
    mario = None
    Flag = False