from . import ActiveSkill
from ..skill_loader import SkillLoader
from ..attack_attribute import AttackAttribute

class AttackAttrXTeamHPAS(ActiveSkill):
    _handle_types = {143}

    def parse_args(self):
        self.multiplier = self.args[0] / 100
        self.attack_attribute = AttackAttribute(self.args[1])
        self.mass_attack = True

    def args_to_json(self):
        return {
            'multiplier': self.multiplier,
            'attack_attribute': self.attack_attribute,
            'mass_attack': self.mass_attack,
        }

    def localize(self):
        return f"Deal {self.multiplier}x Team's HP {self.attack_attribute.name.capitalize()} damage to {'all enemies' if self.mass_attack else '1 enemy'}"
        
    @property
    def active_skill_type(self):
        return 'attack_attr_x_team_hp'


# Register the active skill
SkillLoader._register_active_skill_class(AttackAttrXTeamHPAS)