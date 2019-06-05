from . import ActiveSkill
from ..skill_loader import SkillLoader
from ..region import Region
from ..attack_attribute import AttackAttribute

class CounterAttackAS(ActiveSkill):
    _handle_types = {60}

    def parse_args(self):
        self.duration = self.args[0]
        self.multiplier = self.args[1] / 100
        self.attribute = AttackAttribute(self.args[2])

    def args_to_json(self):
        return {
            'duration': self.duration,
            'multiplier': self.multiplier,
            'attribute': self.attribute,
        }

    def localize(self):
        localization = 'For 1 turn,' if self.duration == 1 else f'For {self.duration} turns,'
        localization += f' perform a {self.attribute.name.capitalize()} counter attack for {self.multiplier}x damage'
        return localization
        
    @property
    def active_skill_type(self):
        return 'counter_attack'


# Register the active skill
SkillLoader._register_active_skill_class(CounterAttackAS)