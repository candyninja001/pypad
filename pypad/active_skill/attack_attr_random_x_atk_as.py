from . import ActiveSkill
from ..skill_loader import SkillLoader
from ..region import Region
from ..attack_attribute import AttackAttribute

class AttackAttrRandomXatkAS(ActiveSkill):
    _handle_types = {58,59}

    def parse_args(self):
        self.attribute = AttackAttribute(self.args[0])
        self.minimum_multiplier = self.args[1] / 100
        self.maximum_multiplier = self.args[2] / 100
        self.mass_attack = self.internal_skill_type == 58

    def args_to_json(self):
        return {
            'attribute': self.attribute.value,
            'minimum_multiplier': self.minimum_multiplier,
            'maximum_multiplier': self.maximum_multiplier,
            'mass_attack': self.mass_attack,
        }

    def localize(self):
        deal = f'Deal {self.minimum_multiplier}x ATK' if self.maximum_multiplier == self.minimum_multiplier else f'Randomly deal {self.minimum_multiplier}x ATK to {self.maximum_multiplier}x ATK'
        return f"{deal} {self.attribute.name.capitalize()} damage to {'all enemies' if self.mass_attack else '1 enemy'}"
        
    @property
    def active_skill_type(self):
        return 'attack_attr_random_x_atk'


# Register the active skill
SkillLoader._register_active_skill_class(AttackAttrRandomXatkAS)