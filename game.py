from brick import Brick
from gameobject import GameObject
from screen import Cell, Screen
import numpy as np
import colorama as col
import config as cfg
from time import sleep, time


class Game:
    def __init__(self) -> None:
        self._screen = Screen()

    def play(self):
        game_ended = False
        brick = Brick(0, (10, 10))
        obj = GameObject(image=[[Cell('i') for _ in range(3)]],
                         vel=(0, 0.6))
        while True:
            frame_st_time = time()
            self._screen.reset_board()
            obj.update_pos()
            self._screen.add_object(obj)
            self._screen.add_object(brick)

            sleep(max(0, cfg.DELAY - (time() - frame_st_time)/1000))
            self._screen.render()
