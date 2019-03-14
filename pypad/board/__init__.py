from .board_size import BoardSize
from .orb_type import OrbType
from .orb_modifier import OrbModifier

class Board:
    def __init__(self, pattern="", board_size=BoardSize.NORMAL):
        self._board_size = board_size
        self.set_pattern(pattern)

    def get_board_size(self):
        self._board_size

    def set_pattern(self, pattern: str):
        self._board_size

    def get_pattern(self):
        self._board_size

    def __str__(self):
        return self.get_pattern()