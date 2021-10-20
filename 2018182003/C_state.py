from enum import Enum

class state(Enum):
    S_idle = 0
    S_move = 1
    S_jump = 2
    S_swim = 3
    S_attaked = 4
    S_die = 5
    S_landing =6

class state_block(Enum):
    S_Idle = 0
    S_Hiting =1
    S_Brocking = 2
    S_Broken = 3
    S_Hited = 4

class Mario_state(Enum):
    mario =0
    Super_mario =1
    Fire_mario = 2
    Growing = 4