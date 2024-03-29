from config import G
from math import cos,  sin
from typing import Tuple
import numpy as np


class GameObject:
    def __init__(self, image: np.ndarray,
                 pos: Tuple[float] = (0, 0),
                 vel: Tuple[float] = (0, 0),
                 gravity: bool = False
                 ) -> None:
        # pos = upperleft coord
        self._img = np.array(image)
        self._pos = np.array(pos, dtype=float)
        self._vel = np.array(vel, dtype=float)
        self._to_remove = False
        self._gravity = gravity

    @property
    def pos(self): return (int(self._pos[0]), int(self._pos[1]))

    @property
    def velx(self): return self._vel[0]

    @property
    def vely(self): return self._vel[1]

    @property
    def vel(self): return self._vel

    @property
    def sizex(self): return self._img.shape[0]

    @property
    def sizey(self): return self._img.shape[1]

    @property
    def horizontal_mid(self): return (self.right_coord + self.left_coord)/2

    @property
    def img(self): return self._img

    @property
    def is_moving_left(self) -> bool: return self._vel[1] < 0

    @property
    def is_moving_up(self) -> bool: return self._vel[0] < 0

    @property
    def is_moving_right(self) -> bool: return self._vel[1] > 0

    @property
    def is_moving_down(self) -> bool: return self._vel[0] > 0

    @property
    def is_moving_leftdown(self) -> bool:
        return self.is_moving_left and self.is_moving_down

    @property
    def is_moving_rightdown(self) -> bool:
        return self.is_moving_right and self.is_moving_down

    @property
    def is_moving_leftup(self) -> bool:
        return self.is_moving_left and self.is_moving_up

    @property
    def is_moving_rightup(self) -> bool:
        return self.is_moving_right and self.is_moving_up

    @property
    def up_coord(self) -> int: return self.pos[0]

    @property
    def down_coord(self) -> int:
        return self.pos[0] + self.img.shape[0] - 1

    @property
    def right_coord(self) -> int: return self.pos[1] + self.img.shape[1] - 1

    @property
    def left_coord(self) -> int: return self.pos[1]

    def to_remove(self): return self._to_remove

    def set_vely(self, new_vel_y):
        self._vel[1] = float(new_vel_y)

    def set_velx(self, new_vel_x):
        self._vel[0] = float(new_vel_x)

    def change_pos(self, newpos):
        self._pos = np.array(newpos)

    def mark_to_remove(self):
        if self._to_remove:
            return False
        self._to_remove = True
        return True

    def update_pos(self):
        ''' Upadates the pos of the obj acc to the vel inside the obj '''
        if self._gravity:
            self._vel[0] = np.around(self._vel[0] + G, 3)

        self._pos = np.around(self._pos + self._vel, 3)

    def deflect(self, theta: float = None, multi_x: float = 1, multi_y: float = 1):
        '''changes velocity using given multipliers or deflect theta degree A-CW'''
        if theta is None:
            try:
                self._vel *= (multi_x, multi_y)
            except:
                print(self._vel)
                print(multi_x, multi_y)
                raise ZeroDivisionError
        else:
            rot_matrix = np.array([
                [cos(theta), sin(theta)],
                [-sin(theta), cos(theta)]
            ])
            self._vel = self._vel @ rot_matrix
        self._pos = np.array(self.pos)


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
    elif (
        (obj1.is_moving_rightdown or obj2.is_moving_leftup) and
        (obj1.right_coord - obj2.left_coord,
         obj1.down_coord - obj2.up_coord) == (-1, -1)
    ):
        return 'rightdown'
    elif (
        (obj1.is_moving_rightup or obj2.is_moving_leftdown) and
        (obj1.right_coord - obj2.left_coord,
         obj1.up_coord - obj2.down_coord) == (-1, 1)
    ):
        return 'rightup'
    elif (
        (obj1.is_moving_leftdown or obj2.is_moving_rightup) and
        (obj1.left_coord - obj2.right_coord,
         obj1.down_coord - obj2.up_coord) == (1, -1)
    ):
        return 'leftdown'
    elif (
        (obj1.is_moving_leftup or obj2.is_moving_rightdown) and
        (obj1.up_coord - obj2.down_coord,
         obj1.left_coord - obj2.right_coord) == (1, 1)
    ):
        return 'leftup'
    return None
 
