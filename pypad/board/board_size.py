from enum import IntEnum

class BoardSize(IntEnum):
    SMALL = 20
    NORMAL = 30
    LARGE = 42

    def __str__(self):
        if self == BoardSize.SMALL:
            return "5x4"
        if self == BoardSize.LARGE:
            return "7x6"
        return "6x5"
