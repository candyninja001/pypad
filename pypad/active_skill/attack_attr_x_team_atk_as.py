from . import ActiveSkill
from .interfaces.attack_asi import AttackASI, AttackDamageCalculationType
from ..skill_loader import SkillLoader
from ..region import Region
from ..attack_attribute import AttackAttribute
from ..common import binary_to_list, iterable_to_string

class AttackAttrXTeamATKAS(ActiveSkill, AttackASI):
    _handle_types = {144}

    def parse_args(self):
        self.team_attributes = tuple(AttackAttribute(a) for a in binary_to_list(self.args[0]))
        self.multiplier = self.args[1] / 100
        self.mass_attack = self.args[2] == 0
        self.attack_attribute = AttackAttribute(self.args[3])

    def args_to_json(self):
        return {
            'team_attributes': self.team_attributes,
            'multiplier': self.multiplier,
            'mass_attack': self.mass_attack,
            'attack_attribute': self.attack_attribute,
        }

    def localize(self):
        attributes_string = iterable_to_string(a.name.capitalize() for a in self.team_attributes)
        return f"Deal {self.multiplier}x Team's {attributes_string} ATK {self.attack_attribute.name.capitalize()} damage to {'all enemies' if self.mass_attack else '1 enemy'}"
        
    @property
    def active_skill_type(self):
        return 'attack_attr_x_team_atk'

    # Interface methods
    def is_attack_mass_attack(self) -> bool:
        return self.mass_attack

    def get_attack_damage_calculation_type(self) -> AttackDamageCalculationType:
        return AttackDamageCalculationType.X_TEAM_ATK

    def get_attack_multipliers(self) -> (float,float):
        return (self.multiplier,self.multiplier)

    def get_attack_team_attributes(self) -> tuple(AttackAttribute):
        return self.team_attributes

    def get_attack_fixed_attack_attribute(self) -> AttackAttribute:
        return self.attack_attribute


# Register the active skill
SkillLoader._register_active_skill_class(AttackAttrXTeamATKAS)