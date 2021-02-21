from math import pi
from os import removedirs
from powerups import PowerUp
from typing import List
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
import copy


class Game:
    def __init__(self) -> None:
        self._screen = Screen()
        self._bricks = basic_brick_layout()

        self._ball_released = False
        self._game_over = False
        self._game_won = None
        self._thru_mode = 0
        self._on_screen_powerups: List[PowerUp] = []
        self._activated_powerups: List[PowerUp] = []

        self._generate_init_ball_paddle()
        self._generate_init_stats()

    @property
    def _objects(self):
        return self._bricks + self._balls + [self._paddle] + self._on_screen_powerups

    def _generate_init_ball_paddle(self):
        self._paddle = Paddle()
        self._balls = [
            Ball(pos=(self._paddle.up_coord-1, self._paddle.horizontal_mid))
        ]

    def set_thru_mode(self):
        self._thru_mode += 1

    def unset_thru_mode(self):
        self._thru_mode -= 1

    def increase_paddle_size(self):
        return self._paddle.increase_size()

    def decrease_paddle_size(self):
        return self._paddle.decrease_size()

    def reset_paddle_size(self):
        return self._paddle.reset_size()

    def speedup_balls(self):
        for ball in self._balls:
            ball.speed_up()

    def reset_speed_balls(self):
        for ball in self._balls:
            ball.reset_speed()

    def duplicate_balls(self):
        new_balls = []
        for ball in self._balls:
            newBall = Ball(pos=ball.pos, vel=(ball.velx, ball.vely))
            newBall.deflect(multi_y=-1)
            new_balls.append(newBall)
        self._balls += new_balls

    def rem_duplicate_balls(self):
        tmp = []
        tot_balls = len(self._balls)
        for i, ball in enumerate(self._balls):
            if i <= np.math.ceil(tot_balls/2):
                tmp.append(ball)
        self._balls = tmp

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
        dead_list: List[Brick] = []
        remain_bricks = []

        for brick in self._bricks:
            if brick.to_remove():
                dead_list.append(brick)
            else:
                remain_bricks.append(brick)
        self._bricks = remain_bricks

        for dead_brick in dead_list:
            if dead_brick.power_up:
                self._on_screen_powerups.append(dead_brick.power_up)

        self._stats.score += len(dead_list)*100
        if not self._bricks:
            self._game_over = True
            self._game_won = True

    def _deactivate_powerups(self):
        remain_powerups = []
        for powerup in self._activated_powerups:
            if time() - powerup.start_time >= powerup.time_out:
                powerup.deactivate(self)
            else:
                remain_powerups.append(powerup)

        self._activated_powerups = remain_powerups

    def _collide_paddle_powerups(self):
        picked = []
        not_picked = []
        for powerup in self._on_screen_powerups:
            if powerup.down_coord == self._paddle.up_coord and (
               self._paddle.right_coord >= powerup.left_coord >= self._paddle.left_coord
               ):
                picked.append(powerup)
            else:
                not_picked.append(powerup)

        self._on_screen_powerups = not_picked
        for powerup in picked:
            powerup.activate(self)
            self._activated_powerups.append(powerup)

    def _remove_not_picked_powerups(self):
        not_removed = []
        for powerup in self._on_screen_powerups:
            if powerup.down_coord < self._screen.height:
                not_removed.append(powerup)
        self._on_screen_powerups = not_removed

    def _remove_lost_balls(self):
        self._balls = list(filter(lambda x: not x.to_remove(), self._balls))
        if not self._balls:
            self._stats.lives -= 1
            self._paddle = Paddle()
            self._generate_init_ball_paddle()
            self._ball_released = False
            if not self._stats.lives:
                self._game_over = True
                self._game_won = False

    def _collide_bricks_ball(self):
        for brick in self._bricks:
            for ball in self._balls:
                hit_side = hit(ball, brick)
                if hit_side in ['right', 'left']:
                    if self._thru_mode > 0:
                        brick.mark_to_remove()
                    else:
                        ball.deflect(multi_y=-1)
                        brick.take_hit()
                elif hit_side in ['up', 'down']:
                    if self._thru_mode > 0:
                        brick.mark_to_remove()
                    else:
                        ball.deflect(multi_x=-1)
                        brick.take_hit()
                elif hit_side is not None:
                    if self._thru_mode > 0:
                        brick.mark_to_remove()
                    else:
                        ball.deflect(multi_x=1, multi_y=-1)
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
            if hit_side in ['down', 'rightdown', 'leftdown']:
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
        final_score = max(0, int(self._stats.score - self.time_passed/10))
        disp_str = "You Won !!" if self._game_won else "You lose :("
        disp_str += '\n'
        disp_str += '\n' + '\t Base score: \t' + str(self._stats.score)
        disp_str += '\n' + '\t Time taken: \t' + str(self.time_passed)
        disp_str += '\n'
        disp_str += '\n' + '\t Final score: \t' + str(final_score)
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

            self._deactivate_powerups()
            self._collide_paddle_powerups()
            self._remove_not_picked_powerups()

            self._collide_ball_paddle()

            for ball in self._balls:
                ball.update_pos()

            for powerup in self._on_screen_powerups:
                powerup.update_pos()

            for obj in self._objects:
                self._screen.add_object(obj)

            if kbhit.kbhit():
                self._handle_inp(kbhit.getch())
            # kbhit.clear()

            sleep(max(0, cfg.DELAY - (time() - frame_st_time)/1000))
            self._screen.render()
            self._render_score_board()
        self._render_end_msg()
