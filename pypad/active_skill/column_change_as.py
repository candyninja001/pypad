from . import ActiveSkill
from ..skill_loader import SkillLoader
from ..region import Region
from ..orb_attribute import OrbAttribute
from ..common import binary_to_list

class ColumnChangeAS(ActiveSkill):
    _handle_types = {127}

    # 0 ->  0  left
    # 1 ->  1  second from left
    # 2 ->  2  thrid from left
    # 3 -> -3  third from right
    # 4 -> -2  second from right
    # 5 -> -1  right
    def _column_index(self, i):
        return i if i < 3 else i - 6

    def parse_args(self):
        self.columns = []
        for indices,orbs in zip(self.args[::2], self.args[1::2]):
            for i in binary_to_list(indices):
                orb_list = tuple(OrbAttribute(o) for o in binary_to_list(orbs))
                self.columns.append((self._column_index(i),orb_list))
        self.columns = tuple(c for c in self.columns)

    def args_to_json(self):
        return {
            'columns': [{'index': c[0], 'orbs': [o.value for o in c[1]]} for c in self.columns]
        }

    def localize(self):
        # eg. 'Change the right column to fire and light orbs and the second to left column to jammer orbs'
        # TODO localize
        return f""
        
    @property
    def active_skill_type(self):
        return 'column_change'


# Register the active skill
SkillLoader._register_active_skill_class(ColumnChangeAS)