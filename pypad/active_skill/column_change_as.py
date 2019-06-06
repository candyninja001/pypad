from enum import Enum
from . import ActiveSkill
from .interfaces.orb_generator_asi import OrbGeneratorASI
from ..skill_loader import SkillLoader
from ..region import Region
from ..orb_attribute import OrbAttribute
from ..common import binary_to_list

class Column(Enum):
    LEFTMOST = 0          # 0 ->  0  left
    SECOND_FROM_LEFT = 1  # 1 ->  1  second from left
    THIRD_FROM_LEFT = 2   # 2 ->  2  thrid from left
    THIRD_FROM_RIGHT = 3  # 3 -> -3  third from right
    SECOND_FROM_RIGHT = 4 # 4 -> -2  second from right
    RIGHTMOST = 5         # 5 -> -1  right

    @classmethod
    def from_json_index(cls, json_index):
        return Column(json_index) if json_index >= 0 else Column(json_index + 6)

    @property
    def json_index(self):
        return self.value if self.value < 3 else self.value - 6

class ColumnChange:
    def __init__(self, column, orbs):
        self.column = Column(column)
        self.orbs = tuple(OrbAttribute(o) for o in orbs)

    def to_json(self):
        return {
            'column': self.column.json_index,
            'orbs': [o.value for o in self.orbs],
        }

class ColumnChangeAS(ActiveSkill, OrbGeneratorASI):
    _handle_types = {127}

    def parse_args(self):
        self.column_changes = []
        for indices,orbs in zip(self.args[::2], self.args[1::2]):
            for i in binary_to_list(indices):
                self.column_changes.append(ColumnChange(i,binary_to_list(orbs)))
        self.column_changes = tuple(cc for cc in self.column_changes)

    def args_to_json(self):
        return {
            'columns': [cc.to_json() for cc in self.column_changes],
        }

    def localize(self):
        # eg. 'Change the right column to fire and light orbs and the second to left column to jammer orbs'
        # TODO localize
        return f""
        
    @property
    def active_skill_type(self):
        return 'column_change'

    # Interface methods
    def does_orb_generator_create_orb_attribute(self, orb_attribute: OrbAttribute) -> bool:
        return any(any(orb_attribute in cc.orbs) for cc in self.column_changes)


# Register the active skill
SkillLoader._register_active_skill_class(ColumnChangeAS)