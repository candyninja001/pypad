from . import LeaderSkill
from ..skill_loader import SkillLoader
from ..orb_attribute import OrbAttribute
from ..common import binary_to_list, optional_multiplier

class MultiConnectedMatchLS(LeaderSkill):
    _handle_types = {192}

    def parse_args(self):
        self.attributes = tuple(OrbAttribute(o) for o in binary_to_list(self.args[0]))
        self.minimum_orbs = self.args[1]

        self.minimum_atk_multiplier = optional_multiplier(self.args[2])
        self.minimum_extra_combo = self.args[3]

            
    def args_to_json(self):
        return {
            'attributes': [o.value for o in self.attributes],
            'minimum_orbs': self.minimum_orbs,
            'minimum_atk_multiplier': self.minimum_atk_multiplier,
            'minimum_extra_combo': self.minimum_extra_combo,
        }

    def localize(self):
        return f"" # TODO note this is the match ALL attributes as x+ orbs, not ANY
        
    @property
    def leader_skill_type(self):
        return 'multi_connected_match'


# Register the active skill
SkillLoader._register_leader_skill_class(MultiConnectedMatchLS)