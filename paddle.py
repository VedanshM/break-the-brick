from config import HEIGHT, PADDLE_STYLE, WIDTH
from typing import Tuple
import numpy as np

from gameobject import GameObject


class Paddle(GameObject):
    '''class for ball in the game'''

    def __init__(self, pos: Tuple = (0.9 * HEIGHT, WIDTH//2)) -> None:
        img = [[PADDLE_STYLE['char']
                for _ in range(PADDLE_STYLE['default_size'])]]
        super().__init__(img, pos=pos, vel=(0, PADDLE_STYLE['init_vel']))

    @property
    def horizontal_mid(self): return (self.right_coord + self.left_coord)/2

    def update_pos(self, to_left: bool = True):
        '''sets paddle to move left or right'''
        self._vel[1] = -abs(self._vel[1]) if to_left else abs(self._vel[1])
        # print(to_left,self._vel)
        self._pos[1] = np.clip(self._pos[1] + self._vel[1],
                               0, WIDTH - self.sizey)
