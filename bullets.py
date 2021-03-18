import gameobject
from typing import Tuple
from utils import create_img
from config import BULLET_STYLE


class Bullet(gameobject.GameObject):
    def __init__(self, pos: Tuple = (0, 0), vel=(0, 0)) -> None:
        super().__init__(create_img(BULLET_STYLE), pos=pos, vel=vel)
