from cell import Cell
import sys
import termios
import atexit
from select import select
import numpy as np
import os


def create_img(data):
    if data['img'] is None:
        return None
    basic_img = np.array(data['img'])
    img = []
    for row in basic_img:
        for char in row:
            img.append(Cell(char, fg=data['fg'], bg=data['bg']))
    img = np.array(img).reshape(basic_img.shape)
    return img


def play_music(path:str):
    os.system(f"aplay -q '{path}' &")

def play_blast():
    return play_music('./audio/blast.wav')

def play_paddle_hit():
    return play_music('./audio/paddle_hit.wav')

def play_ball_launch():
    return play_music('./audio/ball_launch.wav')

def play_level_up():
    return play_music('./audio/level_up.wav')

def play_laser():
    return play_music('./audio/laser.wav')

class KBHit:
    """
    Class to handle keyboard input
    A modified version of "https://stackoverflow.com/a/22085679"
    """

    def __init__(self):
        """
        Creates a KBHit object that you can call to do various keyboard things.
        """
        # Save the terminal settings
        self.__fd = sys.stdin.fileno()
        self.__new_term = termios.tcgetattr(self.__fd)
        self.__old_term = termios.tcgetattr(self.__fd)

        # New terminal setting unbuffered
        self.__new_term[3] = (self.__new_term[3] & ~
                              termios.ICANON & ~termios.ECHO)
        termios.tcsetattr(self.__fd, termios.TCSAFLUSH, self.__new_term)

        # Support normal-terminal reset at exit
        atexit.register(self.set_normal_term)

    def set_normal_term(self):
        """
        Resets to normal terminal
        """
        termios.tcsetattr(self.__fd, termios.TCSAFLUSH, self.__old_term)

    @staticmethod
    def getch():
        """
        Returns a keyboard character after kbhit() has been called.
        Should not be called in the same program as getarrow().
        """
        return sys.stdin.read(1)

    @staticmethod
    def kbhit():
        """
        Returns True if keyboard character was hit, False otherwise.
        """
        return select([sys.stdin], [], [], 0)[0] != []

    @staticmethod
    def clear():
        """
        Clears the input buffer
        """
        termios.tcflush(sys.stdin, termios.TCIFLUSH)


kbhit = KBHit()
