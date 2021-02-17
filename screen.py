from paddle import Paddle
from numpy.lib.npyio import BagObj
from gameobject import GameObject
from cell import Cell
import config as cfg
import colorama as col
import numpy as np


class Screen:
    '''
        This class contorls the screen of the game, i.e. all the rendering part.
    '''

    CLEAR_ALL = '\033[2J'
    GOTO_0 = "\033[0;0H"

    def __init__(self) -> None:
        from os import popen
        rows, cols = tuple(map(int, popen('stty size', 'r').read().split()))
        if rows < cfg.GAME_HEIGHT or cols < cfg.GAME_WIDTH:
            print(Cell(col.Fore.RED, col.Back.WHITE,
                       f"Screen size should be atleast {cfg.GAME_HEIGHT}x{cfg.GAME_WIDTH}"))
            raise SystemExit

        self._width, self._height = cfg.GAME_WIDTH, cfg.GAME_HEIGHT
        self._empty_board = np.full((self._height, self._width), Cell())
        self._board = np.full((self._height, self._width), Cell())

    @property
    def width(self): return self._width

    @property
    def height(self): return self._height

    def reset_board(self):
        np.copyto(self._board, self._empty_board)

    def add_object(self, obj: GameObject) -> bool:
        '''Add a game object to screen board
        '''
        if obj.img is None:
            return False
        img: np.ndarray = obj.img[0: self._height - obj.up_coord,
                                  0: self._width - obj.left_coord]

        if ((img.shape[0] <= 0 or img.shape[1] <= 0) or
            (obj.up_coord >= self._height or obj.left_coord >= self._width)
            ):
            return False
        try:
            self._board[obj.up_coord: obj.down_coord + 1,
                        obj.left_coord: obj.right_coord + 1] = img

        except:
            print(img.shape)
            print(img)
            print(obj.pos)
            raise ValueError
        return True

    def render(self):
        '''Renders the board to the stdout after clearing the screen
        '''
        disp_str = ""
        for row in self._board:
            for cell in row:
                disp_str += str(cell)
            disp_str += '\n'

        print(Screen.CLEAR_ALL + Screen.GOTO_0 + disp_str[:-1])
