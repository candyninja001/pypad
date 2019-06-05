from enum import Enum
from ..common import binary_to_list, gungho_csv, defaultlist
from .floor_modifier import FloorModifierLoader
from .floor_restriction import FloorRestrictionLoader

class DungeonCategory(Enum):
    UNKNOWN = -1
    NORMAL = 0
    SPECIAL = 1
    TECHNICAL = 2
    BONUS = 3
    TOURNAMENT = 4
    MULTIPLAYER_2_PLAYER = 5
    MULTIPLAYER_3_PLAYER = 7

    @classmethod
    def _missing_(cls, value):
        return DungeonCategory.UNKNOWN

class DungeonTab(Enum):
    UNKNOWN = -1
    SPECIAL = 0
    TAB_1 = 1
    TAB_2 = 2
    TAB_3 = 3
    DESCENDED = 101
    COLLAB = 102
    GIFT = 103
    TUTORIAL = 202
    EX_1 = 1001
    EX_2 = 1002
    ARENA = 2000

    @classmethod
    def _missing_(cls, value):
        return DungeonTab.UNKNOWN

class DungeonTag(Enum):
    UNKNOWN = '?'
    NONE = ''
    SOLO = '1'
    QUEST = 'Q'
    COLLAB = 'C'
    GUERRILLA = 'G'

    @classmethod
    def _missing_(cls, value):
        return DungeonTag.UNKNOWN

class DungeonBackground(Enum):
    UNKNOWN = 1

class DungeonInfo:
    def __init__(self, line_id, dungeon_line):
        self.floors = {}
        self.id = int(line_id)
        self.name = dungeon_line[1]
        
        self.tag = DungeonTag.NONE
        if len(self.name) >= 3 and self.name[0] == '#' and self.name[2] == '#':
            self.tag = DungeonTag(self.name[1])
            self.name = self.name[3:]
        
        self.color = '000000' # TODO find default or handle differently
        if len(self.name) >= 8 and self.name[0] == '$' and self.name[7] == '$':
            self.color = self.name[1:7]
            self.name = self.name[8:]

        self.background = int(dungeon_line[2]) # TODO use DungeonBackground
        self.category = DungeonCategory(int(dungeon_line[3]))
        self.sub_category = dungeon_line[4] # TODO use DungeonSubcategory
        self.sort_index = int(dungeon_line[5])
        self.tab = DungeonTab(int(dungeon_line[6]))
        self.sub_tab = dungeon_line[7] # TODO use DungeonSubtab
        self.monster_art = int(dungeon_line[8])

    def _add_floor(self, floor):
        if floor.id in self.floors:
            raise ValueError('Cannot add floor with duplicate floor id')
        self.floors[floor.id] = floor

    def to_json(self):
        return {} # TODO

class FloorUnlockRequirement:
    def __init__(self, dungeon_id, floor_id):
        self.dungeon = dungeon_id
        self.floor = floor_id
    
    def to_json(self):
        return {
            'dungeon': self.dungeon,
            'floor': self.floor,
        }

class FloorInfo:
    def __init__(self, line_id, floor_line):
        self.id = int(line_id)
        self.name = floor_line[1]
        self.battles = int(floor_line[2])
        self.type = int(floor_line[3]) # TODO review
        self.stamina = int(floor_line[4])

        # TODO 5 - 7

        monster = int(floor_line[8])
        i = 0
        self.drops = []
        while monster != 0:
            self.drops.append(monster)
            i += 1
            monster = int(floor_line[i+8])

        bitmap = binary_to_list(int(floor_line[i+9]))
        j = i+10


        if 0 in bitmap:
            self.unlock_requirement = FloorUnlockRequirement(int(floor_line[j]), int(floor_line[j+1]))
            j += 2
        else:
            self.unlock_requirement = FloorUnlockRequirement(0, 0)
        

        # TODO bitmap 1


        if 2 in bitmap:
            j += 1 # TODO


        if 3 in bitmap:
            self.s_rank_score = int(floor_line[j])
            j += 1
        else:
            self.s_rank_score = 0


        if 4 in bitmap:
            j += 1 # TODO


        self.modifiers = []
        if 6 in bitmap:
            modifier_list = [m.split(':') for m in floor_line[j].split('|')]
            
            for m in modifier_list:
                name = m[0]
                value = m[1] if len(m) > 1 else ''
                fm = FloorModifierLoader.load_floor_modifier(name, value)
                if fm != None:
                    self.modifiers.append(fm)

            j += 1

        self.modifiers = tuple(fm for fm in self.modifiers)


        if 5 in bitmap:
            args = [int(x) for x in floor_line[j:]]
            self.restriction = FloorRestrictionLoader.load_floor_restriction(args[0], args[1:])
        else:
            self.restriction = None


    def to_json(self):
        return {} # TODO


class DungeonBook:
    def __init__(self):
        self._dungeons = {}

    def _load(self, dungeon_csv):
        self._dungeons = {}
        current_dungeon_id = 0
        for line in gungho_csv(dungeon_csv):
            line_type = line[0][0:1]
            if line_type == 'c':
                continue # ckey
                
            line_id = int(line[0][2:])

            if line_type == 'd':
                dungeon = DungeonInfo(line_id, defaultlist(int,line))
                current_dungeon_id = dungeon.id
                self._dungeons[dungeon.id] = dungeon

            elif line_type == 'f':
                floor = FloorInfo(line_id, line)
                self._dungeons[current_dungeon_id]._add_floor(floor)


    def __contains__(self, dungeon_id) -> bool:
        return dungeon_id in self._dungeons
    
    def __getitem__(self, dungeon_id) -> DungeonInfo:
        return self._dungeons[dungeon_id]

    def __iter__(self):
        return iter(self._dungeons.values())

    def __len__(self):
        return len(self._dungeons)

    def to_json(self):
        return {str(dungeon_id):dungeon.to_json() for dungeon_id,dungeon in self._dungeons.items()}