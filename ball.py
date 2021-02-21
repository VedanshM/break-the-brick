from math import cos,  sin
from utils import create_img
import paddle
from config import BALL_STYLE
from typing import Tuple
import numpy as np

from gameobject import GameObject


class Ball(GameObject):
    '''class for ball in the game'''

    def __init__(self, pos: Tuple = (0, 0), vel=(0, 0)) -> None:
        super().__init__(create_img(BALL_STYLE), pos=pos, vel=vel)
        self._is_speed_up = 0
        self._org_vel = np.array(BALL_STYLE['vel'])

    def start_moving(self):
        self._vel = self._org_vel

    def stop_moving(self):
        self._org_vel = self._vel
        self._vel = np.array([0, 0])

    def speed_up(self):
        if self._is_speed_up == 0:
            self._vel = np.array([self.velx, self.vely])*2
        self._is_speed_up += 1

    def reset_speed(self):
        self._is_speed_up -= 1
        if self._is_speed_up == 0:
            self._vel = np.array([self.velx, self.vely])/2

    def update_pos(self, pdl: paddle.Paddle = None):
        if pdl is None:
            return super().update_pos()
        else:
            self._pos = (pdl.up_coord - 1, pdl.horizontal_mid)

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
