from bomb import Bomb
from boss import Boss
import math
from bullets import Bullet
from math import inf, pi
from powerups import PowerUp, ShootingPaddle_pu
from typing import List
from utils import kbhit, play_ball_launch, play_blast, play_bounce, play_laser, play_level_up, play_paddle_hit
from paddle import Paddle
from ball import Ball
from brick import Brick, bricks_layout
from gameobject import hit
from screen import Screen
import numpy as np
import config as cfg
from time import sleep, time


class Game:
    def __init__(self) -> None:
        self._screen = Screen()
        self._bricks = bricks_layout(1)

        self._ball_released = False
        self._game_over = False
        self._game_won = None
        self._thru_mode = 0
        self._paddle_grab = 0
        self._on_screen_powerups: List[PowerUp] = []
        self._activated_powerups: List[PowerUp] = []
        self._bullets: List[Bullet] = []
        self._lvl_st_time = 0
        self._time_penalty = 0
        self._mv_down_time = 0

        self._generate_init_ball_paddle()
        self._generate_init_stats()
        self._hit_vel = (0, 0)
        self._boss = None
        self._boss_layers_active = [False, False]
        self._bombs: List[Bomb] = []

    @property
    def _objects(self):
        return (self._bricks + self._balls + [self._paddle]
                + self._on_screen_powerups + self._bullets
                + ([self._boss] if self._boss else [])
                + self._bombs
                )

    def _generate_init_ball_paddle(self):
        self._paddle = Paddle()
        self._balls = [
            Ball(pos=(self._paddle.up_coord-1, self._paddle.horizontal_mid))
        ]

    def set_thru_mode(self):
        self._thru_mode += 1

    def unset_thru_mode(self):
        self._thru_mode -= 1

    def set_paddle_grab(self):
        self._paddle_grab += 1

    def unset_paddle_grab(self):
        self._paddle_grab -= 1

    def increase_paddle_size(self):
        return self._paddle.increase_size()

    def decrease_paddle_size(self):
        return self._paddle.decrease_size()

    def reset_paddle_size(self):
        return self._paddle.reset_size()

    def add_canons(self):
        return self._paddle.add_canons()

    def remove_canons(self):
        return self._paddle.rem_canons()

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

    def _chain_explode(self, st_brick: Brick, bricks: List[Brick]):
        new_dead_list = []

        def is_adj(b1: Brick, b2: Brick):
            for o1, o2 in [(b1, b2), (b2, b1)]:
                if ((
                    o1.down_coord + 1 == o2.up_coord and
                    o2.left_coord - 1 <= o1.left_coord <= o2.right_coord+1)
                    or (
                    o1.up_coord - 1 == o2.down_coord and
                    o2.left_coord - 1 <= o1.left_coord <= o2.right_coord+1)
                    or (
                    o1.left_coord - 1 == o2.right_coord and
                    o1.up_coord - 1 <= o2.up_coord <= o1.up_coord + 1)
                    or (
                    o1.right_coord + 1 == o2.left_coord and
                    o1.up_coord - 1 <= o2.up_coord <= o1.up_coord + 1)
                    ):
                    return True
            return False

        def mark_adj_dead(b: Brick):
            neighs = [br for br in bricks if is_adj(b, br)]
            for x in neighs:
                if x not in new_dead_list:
                    new_dead_list.append(x)
                    if x.is_exploding:
                        mark_adj_dead(x)

        mark_adj_dead(st_brick)
        new_rem_list = [x for x in bricks if x not in new_dead_list]

        return new_dead_list, new_rem_list

    @ property
    def time_passed(self):
        return round((time() - self._lvl_st_time), 1)

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
            play_ball_launch()
            self._ball_released = True
            self._balls[0].start_moving()
        elif ch == 'q':
            self._game_over = True
            self._game_won = False
        elif ch == 'v':
            self._game_over = True
            self._game_won = True

    def _remove_dead_bricks(self):
        dead_list: List[Brick] = []
        remain_bricks = []

        for brick in self._bricks:
            if brick.to_remove():
                dead_list.append(brick)
            else:
                remain_bricks.append(brick)

        for deadBrick in [x for x in dead_list if x.is_exploding]:
            new_dead, new_rem = self._chain_explode(
                deadBrick, remain_bricks)

            dead_list += [x for x in new_dead if x not in dead_list]
            remain_bricks = [x for x in self._bricks if x not in dead_list]
            assert(len(remain_bricks+dead_list) == len(self._bricks))

        self._bricks = remain_bricks

        for dead_brick in dead_list:
            if dead_brick.power_up:
                dead_brick.power_up.start_moving(self._hit_vel)
                self._on_screen_powerups.append(dead_brick.power_up)

        self._stats.score += len(dead_list)*100
        if not list(filter(lambda x: not x.is_unbreakable, self._bricks)) and not self._boss:
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
            for powerup in self._activated_powerups:
                powerup.deactivate(self)
            self._activated_powerups = []
            self._on_screen_powerups = []
            self._paddle = Paddle()
            self._generate_init_ball_paddle()
            self._ball_released = False
            if not self._stats.lives:
                self._game_over = True
                self._game_won = False

    def _collide_powerups_walls(self):
        for powerup in self._on_screen_powerups:
            if powerup.up_coord <= 0 and powerup.is_moving_up:
                powerup.deflect(multi_x=-1)
            if powerup.down_coord + 1 >= self._screen.height and powerup.is_moving_down:
                powerup.mark_to_remove()
            if powerup.left_coord <= 0 and powerup.is_moving_left:
                powerup.deflect(multi_y=-1)
            if powerup.right_coord + 1 >= self._screen.width and powerup.is_moving_right:
                powerup.deflect(multi_y=-1)

    def _collide_bricks_ball(self):
        for brick in self._bricks:
            for ball in self._balls:
                hit_side = hit(ball, brick)

                if hit_side is not None:
                    self._hit_vel = list(ball.vel)[:2]
                    if not brick.is_unbreakable:
                        play_blast()

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

    def _collide_bullet_brick(self):
        for brick in self._bricks:
            for bullet in self._bullets:
                hit_side = hit(bullet, brick)
                if hit_side is not None:
                    self._hit_vel = cfg.POWERUP_GENERAL['vel']
                    bullet.mark_to_remove()
                    brick.take_hit()

    def _remove_marked_bullets(self):
        self._bullets = list(
            filter(lambda x: not x.to_remove(), self._bullets))

    def _collide_bullet_wall(self):
        for bullet in self._bullets:
            if bullet.up_coord == 0:
                bullet.mark_to_remove()

    def _collide_wall_ball(self):
        for ball in self._balls:
            if ball.up_coord <= 0 and ball.is_moving_up:
                play_bounce()
                ball.deflect(multi_x=-1)
            if ball.down_coord + 1 >= self._screen.height and ball.is_moving_down:
                ball.mark_to_remove()
            if ball.left_coord <= 0 and ball.is_moving_left:
                play_bounce()
                ball.deflect(multi_y=-1)
            if ball.right_coord + 1 >= self._screen.width and ball.is_moving_right:
                play_bounce()
                ball.deflect(multi_y=-1)

    def _collide_ball_paddle(self):
        for ball in self._balls:
            hit_side = hit(ball, self._paddle)
            if hit_side in ['down', 'rightdown', 'leftdown']:
                play_paddle_hit()
                delta = (
                    ball.left_coord - self._paddle.horizontal_mid)/self._paddle.sizey
                inci_ang = np.math.atan(abs(ball.velx/ball.vely))

                ref_ang = inci_ang*(1 + delta)
                ref_ang = np.clip(ref_ang, - pi*0.4, pi*0.4)
                ball.deflect(theta=pi - 2*ref_ang)
                if self._paddle_grab > 0:
                    ball.stop_moving()
                    self._ball_released = False

                if time() - self._mv_down_time > cfg.MOVE_DOWN_TIME:
                    self._move_bricks_down()
                    self._mv_down_time = time()

    def _move_bricks_down(self):
        lowest_depth = -1
        for brick in self._bricks:
            brick.change_pos((brick.pos[0]+1, brick.pos[1]))
            lowest_depth = max(lowest_depth, brick.pos[0])

        if lowest_depth >= self._paddle.pos[0]:
            self._game_over = True
            self._game_won = False
            self._stats.lives = 0

    def _render_score_board(self):
        disp_str = (f"Lives: {self._stats.lives} "
                    f"\t\tTime: {self.time_passed} "
                    f"\t\tScore:{self._stats.score}")
        if self._paddle.has_canons:
            st_time = -1
            timeout = 0
            for pu in self._activated_powerups:
                if isinstance(pu, ShootingPaddle_pu):
                    st_time = max(st_time, pu.start_time)
                    timeout = pu.timeout
            disp_str += f'\nShooting paddle time left: {round(timeout - (time () - st_time), 2)}s'
        if self._boss:
            disp_str += f'\nBOSS Health: {self._boss.health}/{self._boss.MAX_HEALTH}'
        print(disp_str)

    def _render_end_msg(self):
        final_score = max(0, int(self._stats.score - self._time_penalty/10))
        disp_str = "You Won !!" if self._game_won else "You lose :("
        disp_str += '\n'
        disp_str += '\n' + '\t Base score: \t' + str(self._stats.score)
        disp_str += '\n' + '\t Time taken: \t' + str(self._time_penalty)
        disp_str += '\n'
        disp_str += '\n' + '\t Final score: \t' + str(final_score)
        Screen.clear_screen()
        print(disp_str)

    def _collide_ball_boss(self):
        if self._boss:
            for ball in self._balls:
                hit_side = hit(ball, self._boss)
                if hit_side is not None:
                    self._hit_vel = list(ball.vel)[:2]
                    print(hit_side)
                    self._boss.take_hit()
                    if hit_side in ['right', 'left']:
                        ball.deflect(multi_y=-1)
                    elif hit_side in ['up', 'down']:
                        ball.deflect(multi_x=-1)
                    else:
                        ball.deflect(multi_x=1, multi_y=-1)

    def _deploy_bricks_layer(self, layer: int = 0):
        if not self._boss or self._boss_layers_active[layer]:
            return

        self._boss_layers_active[layer] = True
        layer_pos = self._boss.down_coord + (2 if layer == 0 else 4)
        for i in range(0, self._screen.width, 3):
            self._bricks.append(
                Brick(1, pos=(layer_pos, i))
            )

    def _position_boss(self):
        if self._boss:
            if self._boss.right_coord < self._paddle.left_coord:
                self._boss.set_vely(self._boss.HORIZ_VEL)
            elif self._boss.left_coord > self._paddle.right_coord:
                self._boss.set_vely(-self._boss.HORIZ_VEL)
            else:
                self._boss.set_vely(0)
            self._boss.update_pos()

    def _drop_bomb(self):
        if not self._boss:
            return
        self._bombs.append(
            Bomb(pos=(self._boss.down_coord, self._boss.horizontal_mid)))

    def _collide_bomb_paddle(self):
        for bomb in self._bombs:
            hit_side = hit(bomb, self._paddle)
            if hit_side is not None:
                self._stats.lives -= 1
                bomb.mark_to_remove()
                if not self._stats.lives:
                    self._game_over = True
                    self._game_won = False

    def _remove_lost_bombs(self):
        for bomb in self._bombs:
            if bomb.down_coord >= self._screen.height:
                bomb.mark_to_remove()
        self._bombs = list(filter(lambda x: not x.to_remove(), self._bombs))

    def _setup_lvl(self, level: int = 1):
        self._bricks = bricks_layout(level)
        self._generate_init_ball_paddle()
        self._ball_released = False
        for pu in self._activated_powerups:
            pu.deactivate(self)
        self._thru_mode = 0
        self._paddle_grab = 0
        self._activated_powerups = []
        self._on_screen_powerups = []
        if level == cfg.BOSS_LVL:
            self._boss = Boss()
            self._position_boss()

    def play(self):
        cur_lvl = 1
        self._mv_down_time = self._lvl_st_time = time()
        bullet_launch_time = 0
        bomb_drop_time = 0
        while not self._game_over:
            frame_st_time = time()
            self._screen.reset_board()

            self._collide_bricks_ball()
            self._collide_bullet_brick()
            self._collide_bullet_wall()
            self._remove_marked_bullets()
            self._remove_dead_bricks()

            self._collide_wall_ball()
            self._remove_lost_balls()

            self._deactivate_powerups()
            self._collide_paddle_powerups()
            self._remove_not_picked_powerups()
            self._collide_powerups_walls()

            self._collide_ball_paddle()

            if self._paddle.has_canons:
                if time() - bullet_launch_time > cfg.BULLET_DELAY:
                    play_laser()
                    bullet1 = Bullet(pos=(self._paddle.up_coord, self._paddle.left_coord),
                                     vel=cfg.BULLET_VELOCITY)
                    bullet2 = Bullet(pos=(self._paddle.up_coord, self._paddle.right_coord),
                                     vel=cfg.BULLET_VELOCITY)
                    self._bullets.append(bullet1)
                    self._bullets.append(bullet2)
                    bullet_launch_time = time()

            if self._boss:
                self._position_boss()
                self._collide_ball_boss()
                if self._boss.health <= self._boss.HEALTH_LIM[1]:
                    self._deploy_bricks_layer(1)
                elif self._boss.health <= self._boss.HEALTH_LIM[0]:
                    self._deploy_bricks_layer(0)
                if time()-bomb_drop_time > cfg.BOMB_DROP_INTERVAL:
                    self._drop_bomb()
                    bomb_drop_time = time()
                self._collide_bomb_paddle()
                self._remove_lost_bombs()
                if self._boss.health == 0:
                    self._game_over = True
                    self._game_won = True


            for brick in self._bricks:
                brick.change_type_if_rainbow()

            for obj in self._balls + self._on_screen_powerups + self._bullets + self._bombs:
                obj.update_pos()

            for obj in self._objects:
                self._screen.add_object(obj)

            if kbhit.kbhit():
                self._handle_inp(kbhit.getch())
            # kbhit.clear()

            sleep(max(0, cfg.DELAY - (time() - frame_st_time)/1000))
            self._screen.render()
            self._render_score_board()

            if self._game_over and self._game_won and cur_lvl < cfg.BOSS_LVL:
                play_level_up()
                self._time_penalty += self.time_passed
                cur_lvl += 1
                self._setup_lvl(cur_lvl)
                self._game_over = False
                self._game_won = False
                self._screen.clear_screen()
                print(f'\n\n Level {cur_lvl -1} Cleared !! GG...')
                sleep(cfg.LVL_MSG_DELAY)
                self._mv_down_time = self._lvl_st_time = time()

        self._render_end_msg()
