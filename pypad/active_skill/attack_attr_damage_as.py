from . import ActiveSkill
from .interfaces.attack_asi import AttackASI, AttackDamageCalculationType
from ..skill_loader import SkillLoader
from ..attack_attribute import AttackAttribute
from ..region import Region

class AttackAttrDamageAS(ActiveSkill, AttackASI):
    _handle_types = {1}

    def parse_args(self):
        self.attribute = AttackAttribute(self.args[0])
        self.damage = self.args[1]
        self.mass_attack = True

    def args_to_json(self):
        return {
            'attribute': self.attribute.value,
            'damage': self.damage,
            'mass_attack': self.mass_attack,
        }

    def localize(self):
        return f"Deal {self.damage} {self.attribute.name.capitalize()} damage to {'all enemies' if self.mass_attack else '1 enemy'}"
        
    @property
    def active_skill_type(self):
        return 'attack_attr_damage'

    # Interface methods
    def is_attack_mass_attack(self) -> bool:
        return self.mass_attack

    def get_attack_damage_calculation_type(self) -> AttackDamageCalculationType:
        return AttackDamageCalculationType.FIXED_DAMAGE

    def get_attack_fixed_damage(self) -> int:
        return self.damage

    def get_attack_fixed_attack_attribute(self) -> AttackAttribute:
        return self.attribute


# Register the active skill
SkillLoader._register_active_skill_class(AttackAttrDamageAS)