from enum import Enum
from .dev import Dev

class OrbSkin(Enum):
    UNKNOWN = -1
    NORMAL_ORBS = 0
    FANCY_ORBS = 1
    VALKYRIE_ORBS = 2
    ZEUS_ORBS = 3
    ATHENA_ORBS = 4
    SHINRABANSHO_CHOCO_ORBS = 5
    GRECO_ROMAN_GODS_ORBS = 6
    SFV_AE_ORBS = 7
    MYSTIC_KNIGHT_ORBS = 8
    HEALER_GIRLS_ORBS = 9
    HERA_ORBS = 10
    YU_YU_HAKUSHO_ORBS = 11
    MONSTER_HUNTER_ORBS = 12
    JAPANESE_GODS_ORBS = 13

    @classmethod
    def _missing_(cls, value):
        Dev.log(f'Unknown orb skin: {value}')
        return OrbSkin.UNKNOWN