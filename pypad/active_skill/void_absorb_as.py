from . import ActiveSkill 
from ..skill_loader import SkillLoader
from ..region import Region
from ..common import iterable_to_string

class VoidAbsorbAS(ActiveSkill):
    _handle_types = {173}

    def parse_args(self):
        self.duration = self.args[0]
        self.attribute_absorb = self.args[1] == 1
        self.damage_absorb = self.args[3] == 1

        if self.args[2] != 0:
            print(f'[VoidAbsorbAS] unexpected args[2]: {self.args[2]}')

    def args_to_json(self):
        return {
            'duration': self.duration,
            'attribute_absorb': self.attribute_absorb,
            'damage_absorb': self.damage_absorb,
        }

    def localize(self):
        absorbs_list = []
        if self.attribute_absorb:
            absorbs_list.append('attribute absorb')
        if self.damage_absorb:
            absorbs_list.append('damage absorb')
        absorbs_string = iterable_to_string(absorbs_list)
        
        localization = 'For 1 turn,' if self.duration == 1 else f'For {self.duration} turns,'
        localization += f' ignore {absorbs_string} effects'
        return localization
        
    @property
    def active_skill_type(self):
        return 'void_absorb'


# Register the active skill
SkillLoader._register_active_skill_class(VoidAbsorbAS)