from enum import Enum

class OrbType(Enum):
    UNKNOWN = -1
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

    _orb_type_characters = {
        -1: ['U'],
         0: ['R'],
         1: ['B'],
         2: ['G'],
         3: ['L'],
         4: ['D'],
         5: ['H'],
         6: ['J'],
         7: ['P'],
         8: ['M'],
         9: ['X','O'],
    }

    def __str__(self):
        return str(self.name).lower().replace('_',' ')

    @classmethod
    def from_character(cls, character):
        for orb_type_value,orb_type_character in cls._orb_type_characters:
            if character in orb_type_character:
                return cls(orb_type_value)
        return cls.UNKNOWN
    
    def to_character(self):
        return OrbType._orb_type_characters[self.value][0]
        