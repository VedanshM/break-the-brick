import colorama
from cell import Cell
from utils import create_img
from config import GAME_HEIGHT, PADDLE_STYLE, GAME_WIDTH
from typing import Tuple
import numpy as np

from gameobject import GameObject


class Paddle(GameObject):
    '''class for ball in the game'''

    def __init__(self, pos: Tuple = (0.9 * GAME_HEIGHT, GAME_WIDTH//2)) -> None:
        img = [create_img(PADDLE_STYLE)]
        super().__init__(img, pos=pos, vel=(0, PADDLE_STYLE['init_vel']))
        self._has_canon = 0

    @property
    def horizontal_mid(self): return (self.right_coord + self.left_coord)/2

    def update_pos(self, to_left: bool = True):
        '''sets paddle to move left or right'''
        self._vel[1] = -abs(self._vel[1]) if to_left else abs(self._vel[1])
        # print(to_left,self._vel)
        self._pos[1] = np.clip(self._pos[1] + self._vel[1],
                               0, GAME_WIDTH - self.sizey)

    def increase_size(self):
        baseCell: Cell = self._img[0][1]
        width = PADDLE_STYLE['default_size'] + PADDLE_STYLE['delta']
        ht = self._img.shape[0]
        self._img = np.full((ht, width), baseCell)
        self._add_cannon_to_img()

    def decrease_size(self):
        baseCell: Cell = self._img[0][1]
        width = PADDLE_STYLE['default_size'] - PADDLE_STYLE['delta']
        ht = self._img.shape[0]
        self._img = np.full((ht, width), baseCell)
        self._add_cannon_to_img()

    def reset_size(self):
        baseCell: Cell = self._img[0][1]
        width = PADDLE_STYLE['default_size']
        ht = self._img.shape[0]
        self._img = np.full((ht, width), baseCell)
        self._add_cannon_to_img()
    
    def _add_cannon_to_img(self):
        if self._has_canon:
            self._img[0][0] = self._img[0][-1] = Cell(char='Y',
                                                  fg=colorama.Fore.LIGHTYELLOW_EX,
                                                  bg=colorama.Back.BLACK)

    @property
    def has_canons(self): return self._has_canon

    def add_canons(self):
        self._has_canon += 1
        if self.has_canons > 0:
            self._add_cannon_to_img()

    def rem_canons(self):
        self._has_canon -= 1
        if self._has_canon == 0:
            self._img = np.array([create_img(PADDLE_STYLE)])
