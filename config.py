HEIGHT, WIDTH = 25, 80

FPS = 15
DELAY = 1/FPS

BRICKS_STYLE = [
    {'img': [['|' for _ in range(3)] for _ in range(3)], 'strength':1},
]

BALL_STYLE = {
    'img': [["o"]],
    'vel': (1/FPS, 1/FPS),
}
