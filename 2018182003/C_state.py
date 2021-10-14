from enum import Enum

class state(Enum):
    S_idle = 0
    S_move = 1
    S_jump = 2
    S_swim = 3
    S_attaked = 4
    S_die = 5
    S_landing =6