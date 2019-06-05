from . import ActiveSkill
from .interfaces.attack_asi import AttackASI, AttackDamageCalculationType
from ..skill_loader import SkillLoader
from ..attack_attribute import AttackAttribute

class DrainAttackXatkAS(ActiveSkill, AttackASI):
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

    # Interface methods
    def is_attack_mass_attack(self) -> bool:
        return self.mass_attack

    def get_attack_damage_calculation_type(self) -> AttackDamageCalculationType:
        return AttackDamageCalculationType.X_ATK

    def get_attack_multipliers(self) -> (float,float):
        return (self.atk_multiplier,self.atk_multiplier)

    def get_attack_fixed_attack_attribute(self) -> AttackAttribute:
        return AttackAttribute.NONE

    def is_attack_drain(self) -> bool:
        return self.recover_multiplier > 0.0

    def get_attack_drain_multiplier(self) -> float:
        return self.recover_multiplier


# Register the active skill
SkillLoader._register_active_skill_class(DrainAttackXatkAS)