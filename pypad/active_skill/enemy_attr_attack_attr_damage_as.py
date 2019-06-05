from . import ActiveSkill
from .interfaces.attack_asi import AttackASI, AttackDamageCalculationType
from ..skill_loader import SkillLoader
from ..region import Region
from ..attack_attribute import AttackAttribute

class EnemyAttrAttackAttrDamageAS(ActiveSkill, AttackASI):
    _handle_types = {42}

    def parse_args(self):
        self.enemy_attribute = AttackAttribute(self.args[0])
        self.attack_attribute = AttackAttribute(self.args[1])
        self.damage = self.args[2]

    def args_to_json(self):
        return {
            'enemy_attribute': self.enemy_attribute,
            'attack_attribute': self.attack_attribute,
            'damage': self.damage,
        }

    def localize(self):
        return f"Deal {self.damage} {self.attack_attribute.name.capitalize()} damage to all {self.enemy_attribute.name.capitalize()} attribute enemies"
        
    @property
    def active_skill_type(self):
        return 'enemy_attr_attack_attr_damage'

    # Interface methods
    def is_attack_mass_attack(self) -> bool:
        return True

    def get_attack_damage_calculation_type(self) -> AttackDamageCalculationType:
        return AttackDamageCalculationType.FIXED_DAMAGE

    def get_attack_fixed_damage(self) -> int:
        return self.damage

    def get_attack_fixed_attack_attribute(self) -> AttackAttribute:
        return self.attack_attribute

    def get_attack_target_attributes(self) -> AttackAttribute:
        return self.enemy_attribute


# Register the active skill
SkillLoader._register_active_skill_class(EnemyAttrAttackAttrDamageAS)