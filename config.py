import colorama


GAME_HEIGHT, GAME_WIDTH = 25, 80
SC_BOARD_HEIGHT, SC_BOARD_WIDTH = 4, GAME_WIDTH

FPS = 60
DELAY = 1/FPS

G = 0.1/FPS

INITIAL_LIVES = 3
MOVE_DOWN_TIME = 3
LVL_MSG_DELAY = 1.4
BOSS_LVL = 3

EXPLODING_BRICK_IDX = 4
BRICK_STRENGHTS = [0, 1, 2, 3, 1, float('inf')]
BRICKS_STYLE = [
    {'img': None,
     'fg': colorama.Fore.GREEN,
     'bg': colorama.Back.LIGHTYELLOW_EX
     },
    {'img': [[':' for _ in range(3)]],
     'fg': colorama.Fore.BLACK,
     'bg': colorama.Back.LIGHTYELLOW_EX
     },
    {'img': [['+' for _ in range(3)]],
     'fg': colorama.Fore.GREEN,
     'bg': colorama.Back.LIGHTYELLOW_EX
     },
    {'img': [['H' for _ in range(3)]],
     'fg': colorama.Fore.BLUE,
     'bg': colorama.Back.LIGHTYELLOW_EX
     },
    {'img': [['*' for _ in range(3)]],
     'fg': colorama.Fore.BLACK,
     'bg': colorama.Back.LIGHTRED_EX
     },
    {'img': [['#' for _ in range(3)]],
     'fg': colorama.Fore.RED,
     'bg': colorama.Back.LIGHTYELLOW_EX
     },
]

BALL_STYLE = {
    'img': [["●"]],
    'fg': colorama.Fore.RED,
    'bg': colorama.Back.LIGHTYELLOW_EX,
    'vel': (-5/FPS, -5/FPS),
}

PADDLE_STYLE = {
    'char': '_',
    'default_size': 7,
    'fg': colorama.Fore.WHITE,
    'bg': colorama.Back.BLACK,
    'init_vel': 60/FPS,
    'delta': 3
}
PADDLE_STYLE['img'] = [PADDLE_STYLE['char']
                       for _ in range(PADDLE_STYLE['default_size'])]

POWERUP_GENERAL = {
    'vel': (5/FPS, 0),
    'timeout': 15,
}

POWERUP_STYLES = [
    {
        'img': [['E']],
        'fg': colorama.Fore.MAGENTA,
        'bg':colorama.Back.LIGHTBLUE_EX
    },
    {
        'img': [['S']],
        'fg': colorama.Fore.MAGENTA,
        'bg':colorama.Back.LIGHTBLUE_EX
    },
    {
        'img': [['2']],
        'fg': colorama.Fore.MAGENTA,
        'bg':colorama.Back.LIGHTBLUE_EX
    },
    {
        'img': [['F']],
        'fg': colorama.Fore.MAGENTA,
        'bg':colorama.Back.LIGHTBLUE_EX
    },
    {
        'img': [['T']],
        'fg': colorama.Fore.MAGENTA,
        'bg':colorama.Back.LIGHTBLUE_EX
    },
    {
        'img': [['P']],
        'fg': colorama.Fore.MAGENTA,
        'bg':colorama.Back.LIGHTBLUE_EX
    },
    {
        'img': [['B']],
        'fg': colorama.Fore.RED,
        'bg': colorama.Back.LIGHTBLUE_EX
    }
]

BULLET_STYLE = {
    'img': [['^']],
    'fg': colorama.Fore.RED,
    'bg': colorama.Back.LIGHTBLUE_EX
}
BULLET_DELAY = 2
BULLET_VELOCITY = (-10/FPS, 0)

BOSS_STYLE = {
    'img': [['=' for _ in range(10)] for _ in range(3)],
    'fg': colorama.Fore.YELLOW,
    'bg': colorama.Back.RED,
    'max_health': 20,
    'horiz_vel':  abs(BALL_STYLE['vel'][1]*0.9),
}

# # for debugging

# FPS = 1
# DELAY = 1/FPS
# BALL_STYLE['vel'] = (0.1/FPS, 0.1/FPS)
# BALL_STYLE['vel'] = (1/FPS, 1/FPS)
