from enum import Enum
from .dev import Dev

class OrbSkin(Enum):
    UNKNOWN = -1
    NORMAL_ORBS = 0
    FANCY_ORBS = 1
    VALKYRIE_ORBS = 2
    ZEUS_ORBS = 3
    ATHENA_ORBS = 4
    KAMEN_RIDER_ORBS = 5
    YOKAI_WATCH_ORBS = 6
    SHINRABANSHO_CHOCO_ORBS = 7
    GRECO_ROMAN_GODS_ORBS = 8
    SFV_AE_ORBS = 9
    MYSTIC_KNIGHT_ORBS = 10
    HEALER_GIRLS_ORBS = 11
    HERA_ORBS = 12
    YU_YU_HAKUSHO_ORBS = 13
    MONSTER_HUNTER_ORBS = 14
    JAPANESE_ORBS = 15
    SHAMAN_KING_ORBS = 16
    SANRIO_CHARACTERS_ORBS = 17
    ATTACK_ON_TITAN_ORBS = 18
    INDIAN_GODS_ORBS = 19

    @classmethod
    def _missing_(cls, value):
        Dev.log(f'Unknown orb skin: {value}')
        return OrbSkin.UNKNOWN