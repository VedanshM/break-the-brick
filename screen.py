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
        if rows < cfg.HEIGHT or cols < cfg.WIDTH:
            print(Cell(col.Fore.RED, col.Back.WHITE,
                       f"Screen size should be atleast {cfg.HEIGHT}x{cfg.WIDTH}"))
            raise SystemExit

        self._width, self._height = cfg.WIDTH, cfg.HEIGHT
        self._empty_board = np.full((self._height, self._width), Cell())
        self._board = np.full((self._height, self._width), Cell())

    def reset_board(self):
        np.copyto(self._board, self._empty_board)

    def add_object(self, object: GameObject) -> bool:
        '''Add a game object to screen board
        '''
        pos, img = object.pos, object.img
        img: np.ndarray = img[:self._height - pos[0], :self._width-pos[1]]

        if (img.shape[0] <= 0 or img.shape[1] <= 0) or (
                pos[0] >= self._height or pos[1] >= self._width):
            return False
        try:
            self._board[pos[0]:pos[0]+img.shape[0],
                        pos[1]:pos[1]+img.shape[1]] = img
        except:
            print(img.shape)
            print(img)
            print(pos)
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

        print(Screen.CLEAR_ALL + Screen.GOTO_0 + disp_str)
