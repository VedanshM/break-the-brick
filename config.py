import colorama


HEIGHT, WIDTH = 25, 80

FPS = 60
DELAY = 1/FPS

BRICK_STRENGHTS = [0, 1, 2, 4, float('inf')]
BRICKS_STYLE = {
    BRICK_STRENGHTS[0]: {'img': [['|' for _ in range(3)]],
                         'fg': colorama.Fore.GREEN,
                         'bg': colorama.Back.LIGHTYELLOW_EX
                         },
    BRICK_STRENGHTS[1]: {'img': [['+' for _ in range(3)]],
                         'fg': colorama.Fore.BLUE,
                         'bg': colorama.Back.LIGHTYELLOW_EX
                         },
    BRICK_STRENGHTS[2]: {'img': [['H' for _ in range(3)]],
                         'fg': colorama.Fore.RED,
                         'bg': colorama.Back.LIGHTYELLOW_EX
                         },
    BRICK_STRENGHTS[-1]: {'img': None},
}

BALL_STYLE = {
    'img': [["o"]],
    'vel': (10/FPS, 10/FPS),
}

PADDLE_STYLE = {
    'char': '=',
    'default_size': 7,
    'init_vel': 60/FPS
}


# # for debugging

# FPS = 1
# DELAY = 1/FPS
# BALL_STYLE['vel'] = (0.1/FPS, 0.1/FPS)
# BALL_STYLE['vel'] = (1/FPS, 1/FPS)
