from typing import Tuple
import numpy as np


class GameObject:
    def __init__(self, image: np.ndarray, pos: Tuple[float] = (0, 0), vel: Tuple[float] = (0, 0)) -> None:
        # pos = upperleft coord
        self._img = np.array(image)
        self._pos = np.array(pos, dtype=float)
        self._vel = np.array(vel, dtype=float)

    @property
    def pos(self): return (int(self._pos[0]), int(self._pos[1]))

    @property
    def img(self): return self._img

    def update_pos(self):
        ''' Upadates the pos of the obj acc to the vel inside the obj '''
        self._pos += self._vel
