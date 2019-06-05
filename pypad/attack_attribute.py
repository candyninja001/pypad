from enum import Enum

class AttackAttribute(Enum):
    NONE = -1
    FIRE = 0
    WATER = 1
    WOOD = 2
    LIGHT = 3
    DARK = 4

    def __ge__(self, other):
        if type(other) == AttackAttribute:
            if self == AttackAttribute.NONE:
                return True
            if other == AttackAttribute.NONE:
                return False
            return self.value >= other.value
        return NotImplemented

    def __gt__(self, other):
        if type(other) == AttackAttribute:
            if other == AttackAttribute.NONE:
                return False
            if self == AttackAttribute.NONE:
                return True
            return self.value > other.value
        return NotImplemented

    def __le__(self, other):
        if type(other) == AttackAttribute:
            if other == AttackAttribute.NONE:
                return True
            if self == AttackAttribute.NONE:
                return False
            return self.value <= other.value
        return NotImplemented

    def __lt__(self, other):
        if type(other) == AttackAttribute:
            if self == AttackAttribute.NONE:
                return False
            if other == AttackAttribute.NONE:
                return True
            return self.value < other.value
        return NotImplemented

    @classmethod
    def _missing_(cls, value):
        return AttackAttribute.NONE

all_attr = (AttackAttribute.FIRE,
            AttackAttribute.WATER,
            AttackAttribute.WOOD,
            AttackAttribute.LIGHT,
            AttackAttribute.DARK)