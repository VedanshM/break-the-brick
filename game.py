from math import pi

from numpy.lib.function_base import angle
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
        self._bricks = [Brick(3, pos=(10, 10))]
        self._balls = [Ball(pos=(20, 40), vel=(1/2, 1/2))]
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
                    brick.take_hit()
                elif hit_side in ['up', 'down']:
                    ball.deflect(multi_x=-1)
                    brick.take_hit()
                elif hit_side is not None:
                    ball.deflect(multi_x=-1, multi_y=-1)
                    brick.take_hit()

        self._bricks = list(filter(lambda x: not x.to_remove(), self._bricks))

    def _collide_wall_ball(self):
        for ball in self._balls:
            if ball.up_coord <= 0 and ball.is_moving_up:
                ball.deflect(multi_x=-1)
            if ball.down_coord + 1 >= self._screen.height and ball.is_moving_down:
                ball.deflect(multi_x=-1)
            if ball.left_coord <= 0 and ball.is_moving_left:
                ball.deflect(multi_y=-1)
            if ball.right_coord + 1 >= self._screen.width and ball.is_moving_right:
                ball.deflect(multi_y=-1)

    def _collide_ball_paddle(self):
        for ball in self._balls:
            hit_side = hit(ball, self._paddle)
            # print(hit_side)
            # print(self._paddle.up_coord, ball.down_coord, ball.is_moving_down)
            # 1/0
            if hit_side == 'down':
                delta = (
                    ball.left_coord - self._paddle.horizontal_mid)/self._paddle.sizex
                inci_ang = np.math.atan(abs(ball.velx/ball.vely))
                ref_ang = inci_ang

                if ball.is_moving_left:
                    ref_ang += (pi/3) * (-delta)
                else:
                    ref_ang += (pi/3) * (delta)

                ball.deflect(theta=pi - 2*ref_ang)

    def play(self):
        game_ended = False

        while not game_ended:
            frame_st_time = time()
            self._screen.reset_board()

            self._collide_bricks_ball()
            self._collide_wall_ball()
            self._collide_ball_paddle()

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
