from .orb_type import OrbType
from .orb_modifier import OrbModifier

class Orb:
    def __init__(self, orb_type, orb_modifiers=0):
        
        self._orb_type = orb_type