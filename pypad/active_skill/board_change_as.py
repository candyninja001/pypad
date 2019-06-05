from . import ActiveSkill
from ..skill_loader import SkillLoader
from ..region import Region
from ..orb_attribute import OrbAttribute
from ..common import iterable_to_string

class BoardChangeAS(ActiveSkill):
    _handle_types = {71}

    def parse_args(self):
        self.orbs = tuple(OrbAttribute(o) for o in self.args if o != -1)

    def args_to_json(self):
        return {
            'orbs': [o.value for o in self.orbs],
        }

    def localize(self):
        orbs_string = iterable_to_string(orb.name.capitalize() for orb in self.orbs)
        return f"Change all orbs to {orbs_string}"
        
    @property
    def active_skill_type(self):
        return 'board_change'


# Register the active skill
SkillLoader._register_active_skill_class(BoardChangeAS)