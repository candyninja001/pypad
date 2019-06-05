from . import ActiveSkill
from .interfaces.attack_asi import AttackASI, AttackDamageCalculationType
from ..skill_loader import SkillLoader
from ..attack_attribute import AttackAttribute
from ..region import Region

class AttackAttrXatkAS(ActiveSkill, AttackASI):
    _handle_types = {0,37}

    @classmethod
    def handles(self, raw_skill):
        return raw_skill[7] > 0

    def parse_args(self):
        self.attribute = AttackAttribute(self.args[0])
        self.multiplier = self.args[1] / 100
        self.mass_attack = self.internal_skill_type == 0

    def args_to_json(self):
        return {
            'attribute': self.attribute.value,
            'multiplier': self.multiplier,
            'mass_attack': self.mass_attack,
        }

    def localize(self):
        return f"Deal {self.multiplier}x ATK {self.attribute.name.capitalize()} damage to {'all enemies' if self.mass_attack else '1 enemy'}"
        
    @property
    def active_skill_type(self):
        return 'attack_attr_x_atk'

    # Interface methods
    def is_attack_mass_attack(self) -> bool:
        return self.mass_attack

    def get_attack_damage_calculation_type(self) -> AttackDamageCalculationType:
        return AttackDamageCalculationType.X_ATK

    def get_attack_multipliers(self) -> (float,float):
        return (self.multiplier,self.multiplier)

    def get_attack_fixed_attack_attribute(self) -> AttackAttribute:
        return self.attribute


# Register the active skill
SkillLoader._register_active_skill_class(AttackAttrXatkAS)