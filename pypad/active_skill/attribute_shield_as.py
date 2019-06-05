from . import ActiveSkill
from ..skill_loader import SkillLoader
from ..region import Region
from ..attack_attribute import AttackAttribute

class AttributeShieldAS(ActiveSkill):
    _handle_types = {21}

    def parse_args(self):
        self.duration = self.args[0]
        self.attribute = AttackAttribute(self.args[1])
        self.reduction = self.args[2] / 100

    def args_to_json(self):
        return {
            'duration': self.duration,
            'attribute': self.attribute,
            'reduction': self.reduction,
        }

    def localize(self):
        localization = 'For 1 turn,' if self.duration == 1 else f'For {self.duration} turns,'
        localization += f' reduce {self.attribute.name.capitalize()} damage by {self.reduction*100}%'
        return localization
        
    @property
    def active_skill_type(self):
        return 'attribute_shield'


# Register the active skill
SkillLoader._register_active_skill_class(AttributeShieldAS)