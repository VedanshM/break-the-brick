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

    @property
    def is_moving_left(self) -> bool: return self._vel[1] < 0

    @property
    def is_moving_up(self) -> bool: return self._vel[0] < 0

    @property
    def is_moving_right(self) -> bool: return self._vel[0] > 0

    @property
    def is_moving_down(self) -> bool: return self._vel[1] > 0

    @property
    def up_coord(self) -> int: return self.pos[0]

    @property
    def down_coord(self) -> int: return self.pos[0] + self.img.shape[0] - 1

    @property
    def right_coord(self) -> int: return self.pos[1] + self.img.shape[1] - 1

    @property
    def left_coord(self) -> int: return self.pos[1]

    def update_pos(self):
        ''' Upadates the pos of the obj acc to the vel inside the obj '''
        self._pos = np.around(self._pos + self._vel, 3)

    # @staticmethod


def hit(obj1: GameObject, obj2: GameObject):

    if ((obj1.is_moving_right or obj2.is_moving_left) and 
            (obj1.right_coord - obj2.left_coord == -1 and
             obj2.up_coord <= obj1.down_coord <= obj2.down_coord)):
        return 'right'

    elif ((obj1.is_moving_down or obj2.is_moving_up) and
            (obj1.down_coord - obj2.up_coord == -1 and
             obj2.left_coord <= obj1.left_coord <= obj2.right_coord)):
        return 'down'
    elif ((obj1.is_moving_left or obj2.is_moving_right) and
            (obj1.left_coord - obj2.right_coord == 1 and
             obj2.up_coord <= obj1.down_coord <= obj2.down_coord)):
        return 'left'
    elif ((obj1.is_moving_up or obj2.is_moving_down) and
            (obj1.up_coord - obj2.down_coord == 1 and
             obj2.left_coord <= obj1.left_coord <= obj2.right_coord)):
        return 'up'
    return None
