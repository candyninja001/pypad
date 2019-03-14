from enum import IntFlag, auto

class OrbModifier(IntFlag):
    ENHANCED = auto()
    LOCKED = auto()
    BLINDED = auto()
    SUPER_BLINDED = auto()
    COMBO_ENHANCED = auto()