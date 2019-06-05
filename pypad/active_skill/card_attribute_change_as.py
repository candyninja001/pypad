from . import ActiveSkill
from ..skill_loader import SkillLoader
from ..region import Region
from ..attack_attribute import AttackAttribute

class CardAttributeChangeAS(ActiveSkill):
    _handle_types = {142}

    def parse_args(self):
        self.duration = self.args[0]
        self.attribute = AttackAttribute(self.args[1])

    def args_to_json(self):
        return {
            'duration': self.duration,
            'attribute': self.attribute.value,
        }

    def localize(self):
        localization = 'For 1 turn,' if self.duration == 1 else f'For {self.duration} turns,'
        localization += f" this cards' attributes change to {self.attribute.name.capitalize()}"
        return localization
        
    @property
    def active_skill_type(self):
        return 'card_attribute_change'


# Register the active skill
SkillLoader._register_active_skill_class(CardAttributeChangeAS)