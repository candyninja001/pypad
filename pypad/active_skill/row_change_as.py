from . import ActiveSkill 
from ..skill_loader import SkillLoader
from ..region import Region
from ..orb_attribute import OrbAttribute
from ..common import binary_to_list

class RowChangeAS(ActiveSkill):
    _handle_types = {128}

    # 0 ->  0  top
    # 1 ->  1  second from top
    # 2 -> -3  third from bottom
    # 3 -> -2  second from bottom
    # 4 -> -1  bottom
    def _row_index(self, i):
        return i if i < 2 else i - 5

    def parse_args(self):
        self.rows = []
        for indices,orbs in zip(self.args[::2], self.args[1::2]):
            for i in binary_to_list(indices):
                orb_list = tuple(OrbAttribute(o) for o in binary_to_list(orbs))
                self.rows.append((self._row_index(i),orb_list))
        self.rows = tuple(r for r in self.rows)

    def args_to_json(self):
        return {
            'rows': [{'index': c[0], 'orbs': [o.value for o in c[1]]} for c in self.rows]
        }

    def localize(self):
        # eg. 'Change the top row to fire and light orbs and the second to bottom row to jammer orbs'
        # TODO localize
        return f""
        
    @property
    def active_skill_type(self):
        return 'row_change'


# Register the active skill
SkillLoader._register_active_skill_class(RowChangeAS)