from . import ActiveSkill
from ..skill_loader import SkillLoader
from ..attack_attribute import AttackAttribute
from ..region import Region

class DamageShieldAS(ActiveSkill):
    _handle_types = {3}

    def parse_args(self):
        self.duration = self.args[0]
        self.reduction = self.args[1] / 100

    def args_to_json(self):
        return {
            'duration': self.duration,
            'reduction': self.reduction,
        }

    def localize(self):
        localization = 'For 1 turn,' if self.duration == 1 else f'For {self.duration} turns,'
        localization += f' reduce damage by {self.reduction*100}%'
        return localization
        
    @property
    def active_skill_type(self):
        return 'damage_shield_buff'


# Register the active skill
SkillLoader._register_active_skill_class(DamageShieldAS)