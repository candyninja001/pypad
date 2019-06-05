from . import ActiveSkill
from ..skill_loader import SkillLoader
from ..region import Region
from ..attack_attribute import AttackAttribute

class AttackAttrGrudgeXatkAS(ActiveSkill):
    _handle_types = {110}

    def parse_args(self):
        self.mass_attack = self.args[0] == 0
        self.attribute = AttackAttribute(self.args[1])
        self.high_hp_multiplier = self.args[2] / 100
        self.low_hp_multiplier = self.args[3] / 100

    def args_to_json(self):
        return {
            'mass_attack': self.mass_attack,
            'attribute': self.attribute.value,
            'high_hp_multiplier': self.high_hp_multiplier,
            'low_hp_multiplier': self.low_hp_multiplier,
        }

    def localize(self):
        deal = f'Deal {self.low_hp_multiplier}x ATK' if self.low_hp_multiplier == self.high_hp_multiplier else f'Deal {self.high_hp_multiplier}x ATK at full hp to {self.low_hp_multiplier}x ATK at 1 hp'
        return f"{deal} {self.attribute.name.capitalize()} damage to {'all enemies' if self.mass_attack else '1 enemy'}"
        
    @property
    def active_skill_type(self):
        return 'attack_attr_grudge_x_atk'


# Register the active skill
SkillLoader._register_active_skill_class(AttackAttrGrudgeXatkAS)