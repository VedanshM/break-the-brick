import colorama as col


class Cell:
    def __init__(self, char=' ', fg=col.Fore.BLACK, bg=col.Back.WHITE) -> None:
        self._char = char
        self._fg = fg
        self._bg = bg

    def __str__(self) -> str:
        return self._fg + self._bg + self._char + col.Style.RESET_ALL
