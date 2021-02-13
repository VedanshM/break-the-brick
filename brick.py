from config import BRICKS_STYLE
from typing import Tuple
import numpy as np

from gameobject import GameObject


class Brick(GameObject):
    '''class for bricks in the game'''

    def __init__(self, type: int = 0, pos: Tuple = (0, 0)) -> None:
        super().__init__(BRICKS_STYLE[type]['img'], pos=pos, vel=(0, 0))
        self._strength = BRICKS_STYLE[type]['strength']
