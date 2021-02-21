from time import time
from typing import Tuple
from utils import create_img
import game
from config import POWERUP_GENERAL, POWERUP_STYLES
import gameobject


class PowerUp(gameobject.GameObject):
    timeout = POWERUP_GENERAL['timeout']

    def __init__(self, img,  pos: Tuple[int, int] = (0, 0)):
        super().__init__(image=img, pos=pos, vel=(POWERUP_GENERAL['vel']))
        self._st_time: float = None

    @property
    def start_time(self): return self._st_time

    @property
    def time_out(self): return self.timeout

    def activate(self, game):
        pass

    def deactivate(self, game):
        pass


class ExpandPaddle_pu(PowerUp):
    def __init__(self,  pos: Tuple[int, int]):
        super().__init__(img=create_img(POWERUP_STYLES[0]),  pos=pos)

    def activate(self, game):
        self._st_time = time()
        game.increase_paddle_size()

    def deactivate(self, game):
        game.reset_paddle_size()


class ShrinkPaddle_pu(PowerUp):
    def __init__(self,  pos: Tuple[int, int]):
        super().__init__(img=create_img(POWERUP_STYLES[1]), pos=pos)

    def activate(self, game):
        self._st_time = time()
        game.decrease_paddle_size()

    def deactivate(self, game):
        game.reset_paddle_size()


class DupliBall_pu(PowerUp):
    def __init__(self,  pos: Tuple[int, int]):
        super().__init__(img=create_img(POWERUP_STYLES[2]), pos=pos)

    def activate(self, game):
        self._st_time = time()
        game.duplicate_balls()

    def deactivate(self, game):
        game.rem_duplicate_balls()


class FastBall_pu(PowerUp):
    def __init__(self,  pos: Tuple[int, int]):
        super().__init__(img=create_img(POWERUP_STYLES[3]), pos=pos)

    def activate(self, game):
        self._st_time = time()
        game.speedup_balls()

    def deactivate(self, game):
        game.reset_speed_balls()
