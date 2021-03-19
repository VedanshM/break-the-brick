from config import BOMB_STYLES
from utils import create_img
import gameobject
from typing import Tuple


class Bomb(gameobject.GameObject):
    def __init__(self, pos: Tuple[float] = (0, 0)):
        super().__init__(image=create_img(BOMB_STYLES),
                         pos=pos, vel=BOMB_STYLES['vel'])
