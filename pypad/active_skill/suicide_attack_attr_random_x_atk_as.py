from . import ActiveSkill 
from ..skill_loader import SkillLoader
from ..region import Region
from ..attack_attribute import AttackAttribute

class SuicideAttackAttrRandomXatkAS(ActiveSkill):
    _handle_types = {84,85}

    def parse_args(self):
        self.attribute = AttackAttribute(self.args[0])
        self.minimum_multiplier = self.args[1] / 100
        self.maximum_multiplier = self.args[2] / 100
        self.remaining_hp_percent = self.args[3] / 100
        self.mass_attack = self.internal_skill_type == 85

    def args_to_json(self):
        return {
            'attribute': self.attribute.value,
            'minimum_multiplier': self.minimum_multiplier,
            'maximum_multiplier': self.maximum_multiplier,
            'remaining_hp_percent': self.remaining_hp_percent,
            'mass_attack': self.mass_attack
        }

    def localize(self):
        localization = f'Deal {self.minimum_multiplier}x ATK' if self.maximum_multiplier == self.minimum_multiplier else f'Randomly deal {self.minimum_multiplier}x ATK to {self.maximum_multiplier}x ATK'
        localization += f" {self.attribute.name.capitalize()} damage to {'all enemies' if self.mass_attack else '1 enemy'}"
        localization += f", but HP is reduced {'to 1' if self.remaining_hp_percent == 0 else f'by {(1.0-self.remaining_hp_percent)*100}%'}"
        return localization
        
    @property
    def active_skill_type(self):
        return 'suicide_attack_attr_random_x_atk'


# Register the active skill
SkillLoader._register_active_skill_class(SuicideAttackAttrRandomXatkAS)