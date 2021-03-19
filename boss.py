from config import BOSS_STYLE
from utils import create_img
import gameobject
from typing import Tuple


class Boss(gameobject.GameObject):
    MAX_HEALTH = BOSS_STYLE['max_health']

    def __init__(self,  pos: Tuple[float] = (0, 0), vel: Tuple[float] = (0, 0)):
        super().__init__(create_img(BOSS_STYLE), pos=pos, vel=vel)
        self._health = Boss.MAX_HEALTH

    @property
    def health(self): return self._health

    def take_hit(self):
        if self._health > 0:
            self._health -= 1
        if self._health == 0:
            self.mark_to_remove()
            return True
        return False
