HEIGHT, WIDTH = 25, 80

FPS = 60
DELAY = 1/FPS

BRICKS_STYLE = [
    {'img': [['|' for _ in range(3)] for _ in range(3)], 'strength':1},
]

BALL_STYLE = {
    'img': [["o"]],
    'vel': (1/FPS, 1/FPS),
}

PADDLE_STYLE = {
    'char': '=',
    'default_size': 4,
    'init_vel': 20/FPS
}
