from enum import Enum
from .dev import Dev

class MonsterType(Enum):
    NONE = -1
    EVO_MATERIAL = 0
    BALANCED = 1
    PHYSICAL = 2
    HEALER = 3
    DRAGON = 4
    GOD = 5
    ATTACKER = 6
    DEVIL = 7
    MACHINE = 8
    AWAKEN_MATERIAL = 12
    ENHANCE_MATERIAL = 14
    REDEEMABLE_MATERIAL = 15

    @classmethod
    def _missing_(cls, value):
        Dev.log(f'Unknown monster type: {value}')
        return MonsterType.UNKNOWN