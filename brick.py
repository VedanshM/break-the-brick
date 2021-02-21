from utils import create_img
from config import BRICKS_STYLE, BRICK_STRENGHTS
from typing import List, Tuple
import numpy as np
import powerups
from gameobject import GameObject


class Brick(GameObject):
    '''class for bricks in the game'''

    power_up_dict = {
        'expand': powerups.ExpandPaddle_pu,
        'shrink': powerups.ShrinkPaddle_pu,
        'dup': powerups.DupliBall_pu,
        'fast': powerups.FastBall_pu,
        'thru': powerups.ThruBall_pu,
        'grab': powerups.PaddleGrab_pu,
    }

    def __init__(self, kind: int = 0,
                 pos: Tuple = (0, 0),
                 powerup: powerups.PowerUp = None,
                 ):
        self._kind = kind
        self._strength = BRICK_STRENGHTS[kind]
        self._powerup = None if powerup is None else (
            self.power_up_dict[powerup](pos)
        )
        self._is_exploding = kind == 4
        super().__init__(create_img(
            BRICKS_STYLE[kind]), pos=pos)

    def take_hit(self):
        self._strength = max(0, self._strength - 1)
        self._kind = BRICK_STRENGHTS.index(self._strength)
        if self._strength <= 0:
            self.mark_to_remove()
            return
        self._img = create_img(BRICKS_STYLE[self._kind])

    @property
    def power_up(self): return self._powerup

    @property
    def is_exploding(self): return self._is_exploding


def basic_brick_layout() -> List[Brick]:
    bricks = []

    for i in np.array(range(10)) + 4:
        for j in np.array(range(4))*3 + 4:
            if i == 13:
                pow_up = 'expand' if j <= 7 else 'shrink'
            else:
                pow_up = None
            bricks.append(Brick(kind=1, pos=(i, j),  powerup=pow_up))

    for i in np.array(range(10)) + 4:
        for j in np.array(range(4))*3 + 20:
            if i == 13:
                pow_up = 'dup' if j <= 23 else 'fast'
            else:
                pow_up = None
            bricks.append(Brick(kind=2, pos=(i, j),  powerup=pow_up))

    for i in np.array(range(10)) + 4:
        for j in np.array(range(4))*3 + 36:
            if i == 13:
                pow_up = 'thru' if j <= 39 else 'grab'
            else:
                pow_up = None
            bricks.append(Brick(kind=3, pos=(i, j),  powerup=pow_up))

    for i in np.array(range(2)) + 14:
        for j in np.array(range(7))*3 + 40:
            bricks.append(Brick(kind=4, pos=(i, j)))

    for i in np.array(range(10)) + 4:
        for j in np.array(range(4))*3 + 52:
            bricks.append(Brick(kind=-1, pos=(i, j)))

    return bricks
