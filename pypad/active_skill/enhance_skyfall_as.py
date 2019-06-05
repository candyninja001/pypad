from . import ActiveSkill
from ..skill_loader import SkillLoader
from ..region import Region

class EnhanceSkyfallAS(ActiveSkill):
    _handle_types = {180}

    def parse_args(self):
        self.duration = self.args[0]
        self.percentage_increase = self.args[1] / 100

    def args_to_json(self):
        return {
            'duration': self.duration,
            'percentage_increase': self.percentage_increase,
        }

    def localize(self):
        localization = 'For 1 turn,' if self.duration == 1 else f'For {self.duration} turns,'
        localization += f' skyfalls have a {self.percentage_increase*100}% chance of being enhanced'
        return localization
        
    @property
    def active_skill_type(self):
        return 'enhance_skyfall'


# Register the active skill
SkillLoader._register_active_skill_class(EnhanceSkyfallAS)