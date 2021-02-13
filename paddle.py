from config import HEIGHT, PADDLE_STYLE, WIDTH
from typing import Tuple
import numpy as np

from gameobject import GameObject


class Paddle(GameObject):
    '''class for ball in the game'''

    def __init__(self, pos: Tuple = (0.9 * HEIGHT, WIDTH//2)) -> None:
        img = [[PADDLE_STYLE['char'] for _ in range(PADDLE_STYLE['def_size'])]]
        super().__init__(img, pos=pos, vel=(0, 0))
