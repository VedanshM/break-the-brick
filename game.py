from math import pi
from utils import kbhit
from paddle import Paddle
from ball import Ball
from brick import Brick, basic_brick_layout
from gameobject import GameObject, hit
from screen import Cell, Screen
import numpy as np
import colorama as col
import config as cfg
from time import process_time_ns, sleep, time


class Game:
    def __init__(self) -> None:
        self._screen = Screen()
        self._bricks = basic_brick_layout()
        self._paddle = Paddle()

        self._ball_released = False
        self._game_over = False
        self._game_won = None

        self._generate_init_ball()
        self._generate_init_stats()

    @property
    def _objects(self):
        return self._bricks + self._balls + [self._paddle]

    def _generate_init_ball(self):
        self._balls = [
            Ball(pos=(self._paddle.up_coord-1, self._paddle.horizontal_mid))
        ]

    @property
    def time_passed(self):
        return round((time() - self._stats.start_time), 1)

    def _generate_init_stats(self):
        def stats(x): return x
        stats.lives = cfg.INITIAL_LIVES
        stats.start_time = time()
        stats.score = 0
        self._stats = stats

    def _handle_inp(self, ch: str):
        ch = ch.lower()
        if ch == 'a':
            self._paddle.update_pos(to_left=True)
            if not self._ball_released:
                self._balls[0].update_pos(pdl=self._paddle)
        elif ch == 'd':
            self._paddle.update_pos(to_left=False)
            if not self._ball_released:
                self._balls[0].update_pos(pdl=self._paddle)
        elif ch == ' ':
            self._ball_released = True
            self._balls[0].start_moving()

    def _remove_dead_bricks(self):
        self._bricks = list(filter(lambda x: not x.to_remove(), self._bricks))
        if not self._bricks:
            self._game_over = True
            self._game_won = True

    def _remove_lost_balls(self):
        self._balls = list(filter(lambda x: not x.to_remove(), self._balls))
        if not self._balls:
            self._game_over = True
            self._game_won = False

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

    def _collide_wall_ball(self):
        for ball in self._balls:
            if ball.up_coord <= 0 and ball.is_moving_up:
                ball.deflect(multi_x=-1)
            if ball.down_coord + 1 >= self._screen.height and ball.is_moving_down:
                ball.mark_to_remove()
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
                    ball.left_coord - self._paddle.horizontal_mid)/self._paddle.sizey
                inci_ang = np.math.atan(abs(ball.velx/ball.vely))

                ref_ang = inci_ang*(1 + delta)
                ref_ang = np.clip(ref_ang, - pi*0.9, pi*0.9)
                ball.deflect(theta=pi - 2*ref_ang)

    def _render_score_board(self):
        disp_str = (f"Lives: {self._stats.lives} "
                    f"\t\tTime: {self.time_passed} "
                    f"\t\tScore:{self._stats.score}")
        print(disp_str)

    def _render_end_msg(self):
        disp_str = "You Won !!" if self._game_won else "You lose :("
        Screen.clear_screen()
        print(disp_str)

    def play(self):
        while not self._game_over:
            frame_st_time = time()
            self._screen.reset_board()

            self._collide_bricks_ball()
            self._remove_dead_bricks()

            self._collide_wall_ball()
            self._remove_lost_balls()

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
            self._render_score_board()
        self._render_end_msg()
