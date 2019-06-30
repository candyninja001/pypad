from . import ActiveSkill 
from ..skill_loader import SkillLoader

class PierceDamageVoidAS(ActiveSkill):
    _handle_types = {191}

    def parse_args(self):
        self.duration = self.args[0]

    def args_to_json(self):
        return {
            'duration': self.duration,
        }

    def localize(self):
        localization = 'For 1 turn,' if self.duration == 1 else f'For {self.duration} turns,'
        localization += f' ignore enemy damage void effects'
        return localization
        
    @property
    def active_skill_type(self):
        return 'pierce_damage_void'


# Register the active skill
SkillLoader._register_active_skill_class(PierceDamageVoidAS)