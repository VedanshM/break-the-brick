import colorama


GAME_HEIGHT, GAME_WIDTH = 25, 80
SC_BOARD_HEIGHT, SC_BOARD_WIDTH = 4, GAME_WIDTH

FPS = 60
DELAY = 1/FPS

INITIAL_LIVES = 3

BRICK_STRENGHTS = [0, 1, 2, 3, float('inf')]
BRICKS_STYLE = {
    BRICK_STRENGHTS[0]: {'img': None,
                         'fg': colorama.Fore.GREEN,
                         'bg': colorama.Back.LIGHTYELLOW_EX
                         },
    BRICK_STRENGHTS[1]: {'img': [[':' for _ in range(3)]],
                         'fg': colorama.Fore.BLACK,
                         'bg': colorama.Back.LIGHTYELLOW_EX
                         },
    BRICK_STRENGHTS[2]: {'img': [['+' for _ in range(3)]],
                         'fg': colorama.Fore.GREEN,
                         'bg': colorama.Back.LIGHTYELLOW_EX
                         },
    BRICK_STRENGHTS[3]: {'img': [['H' for _ in range(3)]],
                         'fg': colorama.Fore.BLUE,
                         'bg': colorama.Back.LIGHTYELLOW_EX
                         },
    BRICK_STRENGHTS[-1]: {'img': [['#' for _ in range(3)]],
                          'fg': colorama.Fore.RED,
                          'bg': colorama.Back.LIGHTYELLOW_EX
                          },
}

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
    'timeout': 5,
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
]

# # for debugging

# FPS = 1
# DELAY = 1/FPS
# BALL_STYLE['vel'] = (0.1/FPS, 0.1/FPS)
# BALL_STYLE['vel'] = (1/FPS, 1/FPS)
