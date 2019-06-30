from . import LeaderSkill
from ..skill_loader import SkillLoader
from ..orb_attribute import OrbAttribute
from ..common import binary_to_list, optional_multiplier, iterable_to_string

class LMatchLS(LeaderSkill):
    _handle_types = {193}

    def parse_args(self):
        self.attributes = tuple(OrbAttribute(o) for o in binary_to_list(self.args[0]))

        self.minimum_atk_multiplier = optional_multiplier(self.args[1])
        self.minimum_damage_reduction = self.args[3]

        # TODO watch args[2] carefully
        # it could be minimum_rcv_multiplier
        # or it could be a pattern type, like 0='L pattern', 1='T pattern', 2='3x3 box pattern'
        # if the latter, this class is PatternMatchLS, not LMatchLS

            
    def args_to_json(self):
        return {
            'attributes': [o.value for o in self.attributes],
            'minimum_atk_multiplier': self.minimum_atk_multiplier,
            'minimum_damage_reduction': self.minimum_damage_reduction,
        }

    def localize(self):
        return f"{self.minimum_atk_multiplier}x ATK and {self.minimum_damage_reduction}% damage reduction when matching {iterable_to_string((a.name.capitalize() for a in self.attributes),'or')} Orbs in an L pattern"
        
    @property
    def leader_skill_type(self):
        return 'l_match'


# Register the active skill
SkillLoader._register_leader_skill_class(LMatchLS)