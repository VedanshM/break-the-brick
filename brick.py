from utils import create_img
from config import BOSS_LVL, BRICKS_STYLE, BRICK_STRENGHTS, EXPLODING_BRICK_IDX
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
        'shoot': powerups.ShootingPaddle_pu,
    }

    def __init__(self, kind: int = 0,
                 pos: Tuple = (0, 0),
                 powerup: powerups.PowerUp = None,
                 rainbow: bool = False
                 ):
        self._kind = kind
        self._strength = BRICK_STRENGHTS[kind]
        self._powerup: powerups.PowerUp = None if powerup is None else (
            self.power_up_dict[powerup](pos)
        )
        self._is_exploding = kind == EXPLODING_BRICK_IDX
        self._is_rainbow = rainbow
        super().__init__(create_img(
            BRICKS_STYLE[kind]), pos=pos)

    def change_type_if_rainbow(self):
        if self._is_rainbow:
            self._kind = max(1, (self._kind+1) % EXPLODING_BRICK_IDX)
            self._strength = BRICK_STRENGHTS[self._kind]
            self._img = create_img(BRICKS_STYLE[self._kind])

    def change_pos(self, newpos):
        self._pos = np.array(newpos)
        if self._powerup:
            self._powerup.change_pos(newpos)

    def take_hit(self):
        self._is_rainbow = False
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


def bricks_layout(lvl: int = 1) -> List[Brick]:
    if lvl == BOSS_LVL:
        return []

    bricks = []

    for i in np.array(range(10)) + 4:
        for j in np.array(range(4))*3 + 4:
            if i == 13:
                pow_up = 'shoot' if j <= 7 else 'expand'
            else:
                pow_up = None
            bricks.append(Brick(kind=1, pos=(i, j),
                                powerup=pow_up, rainbow=(lvl == 2)))

    for i in np.array(range(10)) + 4:
        for j in np.array(range(4))*3 + 20:
            if i == 13:
                pow_up = 'dup' if j <= 23 else 'fast'
            else:
                pow_up = None
            bricks.append(Brick(kind=2, pos=(i, j),
                                powerup=pow_up, rainbow=(lvl == 1)))

    for i in np.array(range(10)) + 4:
        for j in np.array(range(4))*3 + 36:
            if i == 13:
                pow_up = 'thru' if j <= 39 else 'grab'
            else:
                pow_up = None
            bricks.append(Brick(kind=3, pos=(i, j),  powerup=pow_up))

    for i in np.array(range(2)) + 14:
        for j in np.array(range(7))*3 + (40 if lvl == 1 else 20):
            bricks.append(Brick(kind=4, pos=(i, j)))

    for i in np.array(range(10)) + 4:
        for j in np.array(range(4))*3 + 52:
            bricks.append(Brick(kind=-1, pos=(i, j)))

    return bricks
