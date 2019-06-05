from . import ActiveSkill
from .interfaces.attack_asi import AttackASI, AttackDamageCalculationType
from ..skill_loader import SkillLoader
from ..attack_attribute import AttackAttribute

class AttackXatkAS(ActiveSkill, AttackASI):
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

    # Interface methods
    def is_attack_mass_attack(self) -> bool:
        return self.mass_attack

    def get_attack_damage_calculation_type(self) -> AttackDamageCalculationType:
        return AttackDamageCalculationType.X_ATK

    def get_attack_multipliers(self) -> (float,float):
        return (self.multiplier,self.multiplier)

    def get_attack_fixed_attack_attribute(self) -> AttackAttribute:
        return AttackAttribute.NONE


# Register the active skill
SkillLoader._register_active_skill_class(AttackXatkAS)