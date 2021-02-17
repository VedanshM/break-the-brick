from math import atan, cos, pi, sin
from config import BALL_STYLE
from typing import Tuple
import numpy as np

from gameobject import GameObject


class Ball(GameObject):
    '''class for ball in the game'''

    def __init__(self, pos: Tuple = (0, 0), vel: Tuple = BALL_STYLE['vel']) -> None:
        super().__init__(BALL_STYLE['img'], pos=pos, vel=vel)

    def deflect(self, theta: float = None, multi_x: float = 1, multi_y: float = 1):
        '''changes velocity of the ball using given multipliers or deflect theta degree A-CW'''
        if theta is None:
            self._vel *= (multi_x, multi_y)
        else:
            rot_matrix = np.array([
                [cos(theta), sin(theta)],
                [-sin(theta), cos(theta)]
            ])
            self._vel = self._vel @ rot_matrix
        self._pos = np.array(self.pos)
