from enum import Enum
from . import ActiveSkill 
from .interfaces.orb_generator_asi import OrbGeneratorASI
from ..skill_loader import SkillLoader
from ..orb_attribute import OrbAttribute
from ..common import binary_to_list

class Row(Enum):
    TOPMOST = 0            # 0 ->  0  top
    SECOND_FROM_TOP = 1    # 1 ->  1  second from top
    THIRD_FROM_BOTTOM = 2  # 2 -> -3  third from bottom
    SECOND_FROM_BOTTON = 3 # 3 -> -2  second from bottom
    BOTTOMMOST = 4         # 4 -> -1  bottom

    @classmethod
    def from_json_index(cls, json_index):
        return Row(json_index) if json_index >= 0 else Row(json_index + 5)

    @property
    def json_index(self):
        return self.value if self.value < 2 else self.value - 5

class RowChange:
    def __init__(self, row, orbs):
        self.row = Row(row)
        self.orbs = tuple(OrbAttribute(o) for o in orbs)

    def to_json(self):
        return {
            'row': self.row.json_index,
            'orbs': [o.value for o in self.orbs],
        }

class RowChangeAS(ActiveSkill, OrbGeneratorASI):
    _handle_types = {128}

    def parse_args(self):
        self.row_changes = []
        for indices,orbs in zip(self.args[::2], self.args[1::2]):
            for i in binary_to_list(indices):
                self.row_changes.append(RowChange(i,binary_to_list(orbs)))
        self.row_changes = tuple(rc for rc in self.row_changes)

    def args_to_json(self):
        return {
            'rows': [rc.to_json() for rc in self.row_changes]
        }

    def localize(self):
        # eg. 'Change the top row to fire and light orbs and the second to bottom row to jammer orbs'
        # TODO localize
        return f""
        
    @property
    def active_skill_type(self):
        return 'row_change'

    # Interface methods
    def does_orb_generator_create_orb_attribute(self, orb_attribute: OrbAttribute) -> bool:
        return any(any(orb_attribute in rc.orbs) for rc in self.row_changes)


# Register the active skill
SkillLoader._register_active_skill_class(RowChangeAS)