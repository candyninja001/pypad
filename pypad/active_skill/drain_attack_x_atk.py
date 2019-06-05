from . import ActiveSkill
from ..skill_loader import SkillLoader
from ..region import Region

class DrainAttackXatkAS(ActiveSkill):
    _handle_types = {35}

    def parse_args(self):
        self.atk_multiplier = self.args[0] / 100
        self.recover_multiplier = self.args[1] / 100
        self.mass_attack = False

    def args_to_json(self):
        return {
            'atk_multiplier': self.atk_multiplier,
            'recover_multiplier': self.recover_multiplier,
            'mass_attack': self.mass_attack,
        }

    def localize(self):
        return f"Deal {self.atk_multiplier}x ATK damage to 1 enemy and recover {self.recover_multiplier}x damage dealt as HP"
        
    @property
    def active_skill_type(self):
        return 'drain_attack_x_atk'


# Register the active skill
SkillLoader._register_active_skill_class(DrainAttackXatkAS)