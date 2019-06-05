from . import ActiveSkill
from ..skill_loader import SkillLoader
from ..region import Region

class AttackXatkAS(ActiveSkill):
    _handle_types = {2}

    def parse_args(self):
        self.multiplier = self.args[1] / 100
        self.mass_attack = False

    def args_to_json(self):
        return {
            'multiplier': self.multiplier,
            'mass_attack': False,
        }

    def localize(self):
        return f"Deal {self.multiplier}x ATK damage to {'all enemies' if self.mass_attack else '1 enemy'}"
        
    @property
    def active_skill_type(self):
        return 'attack_x_atk'


# Register the active skill
SkillLoader._register_active_skill_class(AttackXatkAS)