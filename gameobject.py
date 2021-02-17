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
    def is_moving_right(self) -> bool: return not self.is_moving_left

    @property
    def is_moving_down(self) -> bool: return not self.is_moving_up

    @property
    def up_coord(self) -> int: return self.pos[0]

    @property
    def down_coord(self) -> int: return self.pos[0] + self.img.shape[0]

    @property
    def right_coord(self) -> int: return self.pos[1] + self.img.shape[1]

    @property
    def left_coord(self) -> int: return self.pos[1]

    def update_pos(self):
        ''' Upadates the pos of the obj acc to the vel inside the obj '''
        self._pos = np.around(self._pos+  self._vel, 3)

    @staticmethod
    def overlap(obj1, obj2):
        return not(
            (obj1.up_coord >= obj2.down_coord) or
            (obj2.up_coord >= obj1.down_coord) or
            (obj2.left_coord >= obj1.right_coord) or
            (obj1.left_coord >= obj2.right_coord)
        )

        # return not ((
        #     pos1[0] > pos2[0] + size2[0]) or (
        #     pos2[0] > pos1[0] + size1[0]) or (
        #     pos1[1] > pos2[1] + size2[1]) or (
        #     pos2[1] > pos1[1] + size1[1]
        # ))
