from . import ActiveSkill 
from ..skill_loader import SkillLoader
from ..region import Region

class MassAttackAS(ActiveSkill):
    _handle_types = {51}

    def parse_args(self):
        self.duration = self.args[0]

    def args_to_json(self):
        return {
            'duration': self.duration,
        }

    def localize(self):
        return 'For 1 turn, all attacks are mass attacks' if self.duration == 1 else f'For {self.duration} turns, all attacks are mass attacks'
        
    @property
    def active_skill_type(self):
        return 'mass_attack_buff'


# Register the active skill
SkillLoader._register_active_skill_class(MassAttackAS)