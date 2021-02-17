import sys
from utils import kbhit
from paddle import Paddle
from ball import Ball
from brick import Brick
from gameobject import GameObject, hit
from screen import Cell, Screen
import numpy as np
import colorama as col
import config as cfg
from time import sleep, time


class Game:
    def __init__(self) -> None:
        self._screen = Screen()
        self._bricks = [Brick(0, (10, 10))]
        self._balls = [Ball(pos=(10, 8))]
        self._paddle = Paddle()

    @property
    def _objects(self):
        return self._bricks + self._balls + [self._paddle]

    def _handle_inp(self, ch: str):
        ch = ch.lower()
        if ch == 'a':
            self._paddle.update_pos(to_left=True)
        if ch == 'd':
            self._paddle.update_pos(to_left=False)

    def _collide_bricks_ball(self):
        for brick in self._bricks:
            for ball in self._balls:
                hit_side = hit(ball, brick)
                if hit_side in ['right', 'left']:
                    ball.deflect(multi_y=-1)
                elif hit_side in ['up', 'down']:
                    ball.deflect(multi_x=-1)

    def _collide_wall_ball(self):
        for ball in self._balls:
            if ball.up_coord < 0:
                ball.deflect(multi_x=-1)
            if ball.down_coord > self._screen.height:
                ball.deflect(multi_x=-1)
            if ball.left_coord < 0:
                ball.deflect(multi_y=-1)
            if ball.right_coord > self._screen.width:
                ball.deflect(multi_y=-1)

    def play(self):
        game_ended = False

        while not game_ended:
            frame_st_time = time()
            self._screen.reset_board()

            self._collide_bricks_ball()
            self._collide_wall_ball()

            for ball in self._balls:
                ball.update_pos()

            for obj in self._objects:
                self._screen.add_object(obj)

            if kbhit.kbhit():
                self._handle_inp(kbhit.getch())
            # kbhit.clear()

            sleep(max(0, cfg.DELAY - (time() - frame_st_time)/1000))
            self._screen.render()
            ball = self._balls[0]
            print(ball.pos, ball._pos, ball._vel)
