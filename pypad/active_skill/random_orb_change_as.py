from . import ActiveSkill 
from ..skill_loader import SkillLoader
from ..region import Region
from ..orb_attribute import OrbAttribute
from ..common import binary_to_list, iterable_to_string

class RandomOrbChangeAS(ActiveSkill):
    _handle_types = {154}

    def parse_args(self):
        self.from_orbs = tuple(OrbAttribute(o) for o in binary_to_list(self.args[0]))
        self.to_orbs = tuple(OrbAttribute(o) for o in binary_to_list(self.args[1]))

    def args_to_json(self):
        return {
            'from_orbs': [o.value for o in self.from_orbs],
            'to_orbs': [o.value for o in self.to_orbs],
        }

    def localize(self):
        from_orbs_string = iterable_to_string(o.name.capitalize() for o in self.from_orbs)
        to_orbs_string = iterable_to_string(o.name.capitalize() for o in self.to_orbs)
        return f"Change {from_orbs_string} orbs to {to_orbs_string} orbs"
        
    @property
    def active_skill_type(self):
        return 'random_orb_change'


# Register the active skill
SkillLoader._register_active_skill_class(RandomOrbChangeAS)