from . import ActiveSkill
from ..skill_loader import SkillLoader
from ..region import Region
from ..orb_attribute import OrbAttribute
from ..common import binary_to_list

class EnhanceOrbsAS(ActiveSkill):
    _handle_types = {52,91,140}

    def parse_args(self):
        if self.internal_skill_type == 51:
            self.orbs = (OrbAttribute(self.args[0]),)
        if self.internal_skill_type == 91:
            self.orbs = tuple(OrbAttribute(a) for a in self.args[0:2])
        if self.internal_skill_type == 140:
            self.orbs = tuple(OrbAttribute(a) for a in binary_to_list(self.args[0]))

    def args_to_json(self):
        return {
            'orbs': [o.value for o in self.orbs]
        }

    def localize(self):
        orb_list = [orb.name.capitalize() for orb in self.orbs]
        orbs_string = ''
        if len(self.orbs) == 1:
            orbs_string = orb_list[0]
        else:
            orbs_string = ', '.join(orb for orb in orb_list[:-1]) + f' and {orb_list[-1]}'
        return f'Enhance all {orbs_string} orbs'
        
    @property
    def active_skill_type(self):
        return 'enhance_orbs'


# Register the active skill
SkillLoader._register_active_skill_class(EnhanceOrbsAS)