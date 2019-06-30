from enum import Enum
from .dev import Dev

class OrbAttribute(Enum):
    UNKNOWN = -2
    NONE = -1
    FIRE = 0
    WATER = 1
    WOOD = 2
    LIGHT = 3
    DARK = 4
    HEAL = 5
    JAMMER = 6
    POISON = 7
    MORTAL_POISON = 8
    BOMB = 9

    @classmethod
    def _missing_(cls, value):
        Dev.log(f'Unknown orb attribute: {value}')
        return OrbAttribute.UNKNOWN