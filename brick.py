from utils import create_img
from cell import Cell
from config import BRICKS_STYLE, BRICK_STRENGHTS
from typing import List, Tuple
import numpy as np

from gameobject import GameObject


class Brick(GameObject):
    '''class for bricks in the game'''

    def __init__(self, kind: int = 0, pos: Tuple = (0, 0)) -> None:
        self._strength = BRICK_STRENGHTS[kind]
        super().__init__(create_img(
            BRICKS_STYLE[self._strength]), pos=pos)

    def take_hit(self):
        self._strength -= 1
        if self._strength == 0:
            self.mark_to_remove()
        self._img = create_img(BRICKS_STYLE[self._strength])


def basic_brick_layout() -> List[Brick]:
    bricks = []

    for i in np.array(range(10)) + 4:
        for j in np.array(range(4))*3 + 4:
            bricks.append(Brick(kind=1, pos=(i, j)))

    for i in np.array(range(10)) + 4:
        for j in np.array(range(4))*3 + 20:
            bricks.append(Brick(kind=2, pos=(i, j)))

    for i in np.array(range(10)) + 4:
        for j in np.array(range(4))*3 + 36:
            bricks.append(Brick(kind=3, pos=(i, j)))

    for i in np.array(range(10)) + 4:
        for j in np.array(range(4))*3 + 52:
            bricks.append(Brick(kind=-1, pos=(i, j)))

    return bricks
