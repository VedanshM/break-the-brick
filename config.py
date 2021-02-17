HEIGHT, WIDTH = 25, 80

FPS = 60
DELAY = 1/FPS

BRICKS_STYLE = [
    {'img': [['|' for _ in range(3)] for _ in range(3)], 'strength':1},
]

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
