import sys
from utils import kbhit
from paddle import Paddle
from ball import Ball
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
        self._bricks = [Brick(0, (10, 10))]
        self._balls = [Ball(pos=(9, 9))]
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
        def handle_collison(brick: Brick, ball: Ball):
            if ball.is_moving_right:
                if ball.right_coord > brick.left_coord:
                    ball.deflect(multi_x=-1)

                elif ball.down_coord > brick.up_coord and ball.is_moving_down:
                    ball.deflect(multi_y=-1)

                elif ball.up_coord < brick.down_coord and ball.is_moving_up:
                    ball.deflect(multi_y=-1)

                else:
                    assert(False, 'collision maybe has not happened')
            elif ball.is_moving_left:
                if ball.left_coord < brick.right_coord:
                    ball.deflect(multi_x=-1)

                elif ball.is_moving_down and ball.down_coord > brick.up_coord:
                    ball.deflect(multi_y=-1)

                elif ball.is_moving_up and ball.up_coord < brick.down_coord:
                    ball.deflect(multi_y=-1)

                else:
                    assert(False, 'collision maybe has not happened')
            else:
                assert(False, 'error in is_moving funcs')

        for brick in self._bricks:
            for ball in self._balls:
                if GameObject.overlap(brick, ball):
                    handle_collison(brick, ball)

    def play(self):
        game_ended = False

        while not game_ended:
            frame_st_time = time()
            self._screen.reset_board()

            self._collide_bricks_ball()

            for ball in self._balls:
                ball.update_pos()

            for obj in self._objects:
                self._screen.add_object(obj)

            if kbhit.kbhit():
                self._handle_inp(kbhit.getch())
            kbhit.clear()

            sleep(max(0, cfg.DELAY - (time() - frame_st_time)/1000))
            self._screen.render()
            ball = self._balls[0]
            print(ball.pos, ball._pos, ball._vel)
