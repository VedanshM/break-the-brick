from config import BALL_STYLE
from typing import Tuple
import numpy as np

from gameobject import GameObject


class Ball(GameObject):
    '''class for ball in the game'''

    def __init__(self, pos: Tuple = (0, 0), vel: Tuple = BALL_STYLE['vel']) -> None:
        super().__init__(BALL_STYLE['img'], pos=pos, vel=vel)
