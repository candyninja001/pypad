from enum import Enum

class Region(Enum):
    JP = 0
    NA = 1
    
    def name(self):
        if self == Region.JP:
            return 'jp'
        if self == Region.NA:
            return 'na'
        return 'error'