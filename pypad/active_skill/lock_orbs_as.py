from . import ActiveSkill 
from ..skill_loader import SkillLoader
from ..region import Region
from ..orb_attribute import OrbAttribute
from ..common import binary_to_list, iterable_to_string

class LockOrbsAS(ActiveSkill):
    _handle_types = {152}

    def parse_args(self):
        self.orbs = tuple(OrbAttribute(o) for o in binary_to_list(self.args[0]))

    def args_to_json(self):
        return {
            'orbs': [o.value for o in self.orbs]
        }

    def localize(self):
        orbs_string = iterable_to_string(o.name.capitalize() for o in self.orbs)
        return f"Lock {orbs_string} orbs"
        
    @property
    def active_skill_type(self):
        return 'lock_orbs'


# Register the active skill
SkillLoader._register_active_skill_class(LockOrbsAS)