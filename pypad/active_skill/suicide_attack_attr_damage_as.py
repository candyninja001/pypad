from . import ActiveSkill
from .interfaces.attack_asi import AttackASI, AttackDamageCalculationType
from .interfaces.suicide_asi import SuicideASI
from ..skill_loader import SkillLoader
from ..region import Region
from ..attack_attribute import AttackAttribute

class SuicideAttackAttrDamageAS(ActiveSkill, AttackASI, SuicideASI):
    _handle_types = {86,87}

    def parse_args(self):
        self.attribute = AttackAttribute(self.args[0])
        self.damage = self.args[1]
        # self.args[2] unused?
        self.remaining_hp_percent = self.args[3] / 100
        self.mass_attack = self.internal_skill_type == 87

    def args_to_json(self):
        return {
            'attribute': self.attribute.value,
            'damage': self.damage,
            'remaining_hp_percent': self.remaining_hp_percent,
            'mass_attack': self.mass_attack
        }

    def localize(self):
        localization = f"Deal {self.damage} {self.attribute.name.capitalize()} damage to {'all enemies' if self.mass_attack else '1 enemy'}"
        localization += f", but HP is reduced {'to 1' if self.remaining_hp_percent == 0 else f'by {(1.0-self.remaining_hp_percent)*100}%'}"
        return localization
        
    @property
    def active_skill_type(self):
        return 'suicide_attack_attr_damage'

    # Interface methods
    def is_attack_mass_attack(self) -> bool:
        return self.mass_attack

    def get_attack_damage_calculation_type(self) -> AttackDamageCalculationType:
        return AttackDamageCalculationType.FIXED_DAMAGE

    def get_attack_fixed_damage(self) -> int:
        return self.damage

    def get_attack_fixed_attack_attribute(self) -> AttackAttribute:
        return self.attribute

    def is_suicide(self) -> bool:
        return self.remaining_hp_percent < 1.0

    def get_suicide_percentage(self) -> float:
        return self.remaining_hp_percent


# Register the active skill
SkillLoader._register_active_skill_class(SuicideAttackAttrDamageAS)