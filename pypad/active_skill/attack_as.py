from . import ActiveSkill
from enum import Enum
from .interfaces.suicide_asi import SuicideASI
from ..skill_loader import SkillLoader
from ..attack_attribute import AttackAttribute
from ..common import binary_to_list

class AttackDamageCalculationType(Enum):
    UNKNOWN = 'unknown'
    FIXED_DAMAGE = 'fixed_damage'
    X_ATK = 'x_atk'
    X_TEAM_ATK = 'x_team_atk'
    X_TEAM_HP = 'x_team_hp'
    GRUDGE_X_ATK = 'grudge_x_atk'
    RANDOM_X_ATK = 'random_x_atk'

class AttackAS(ActiveSkill, SuicideASI):
    _handle_types = {0,1,2,35,37,42,58,59,84,85,86,87,110,115,143,144}

    def parse_args(self):
        self.damage_calculation_type = AttackDamageCalculationType.UNKNOWN
        self.mass_attack = True
        self.x_team_atk_attributes = tuple()
        self.attack_attribute = AttackAttribute.NONE
        self.target_attribute = AttackAttribute.NONE
        self.fixed_damage = 0
        self.minimum_multiplier = 0.0
        self.maximum_multiplier = 0.0
        self.suicide_hp_remaining = 1.0
        self.drain_multiplier = 0.0

        if self.internal_skill_type == 0:
            self.damage_calculation_type = AttackDamageCalculationType.X_ATK
            self.mass_attack = True
            self.attack_attribute = AttackAttribute(self.args[0])
            self.minimum_multiplier = self.args[1] / 100
            self.maximum_multiplier = self.args[1] / 100

        if self.internal_skill_type == 1:
            self.damage_calculation_type = AttackDamageCalculationType.FIXED_DAMAGE
            self.mass_attack = True
            self.attack_attribute = AttackAttribute(self.args[0])
            self.fixed_damage = self.args[1]

        if self.internal_skill_type == 2:
            self.damage_calculation_type = AttackDamageCalculationType.X_ATK
            self.mass_attack = False
            self.multiplier = self.args[1] / 100

        if self.internal_skill_type == 35:
            self.damage_calculation_type = AttackDamageCalculationType.X_ATK
            self.mass_attack = False
            self.minimum_multiplier = self.args[0] / 100
            self.maximum_multiplier = self.args[0] / 100
            self.drain_multiplier = self.args[1] / 100

        if self.internal_skill_type == 37:
            self.damage_calculation_type = AttackDamageCalculationType.X_ATK
            self.mass_attack = False
            self.attack_attribute = AttackAttribute(self.args[0])
            self.minimum_multiplier = self.args[1] / 100
            self.maximum_multiplier = self.args[1] / 100

        if self.internal_skill_type == 42:
            self.internal_skill_type = AttackDamageCalculationType.FIXED_DAMAGE
            self.mass_attack = True
            self.target_attribute = AttackAttribute(self.args[0])
            self.attack_attribute = AttackAttribute(self.args[1])
            self.fixed_damage = self.args[2]

        if self.internal_skill_type == 58:
            self.damage_calculation_type = AttackDamageCalculationType.RANDOM_X_ATK
            self.mass_attack = True
            self.attack_attribute = AttackAttribute(self.args[0])
            self.minimum_multiplier = self.args[1] / 100
            self.maximum_multiplier = self.args[2] / 100

        if self.internal_skill_type == 59:
            self.damage_calculation_type = AttackDamageCalculationType.RANDOM_X_ATK
            self.mass_attack = False
            self.attack_attribute = AttackAttribute(self.args[0])
            self.minimum_multiplier = self.args[1] / 100
            self.maximum_multiplier = self.args[2] / 100

        if self.internal_skill_type == 84:
            self.damage_calculation_type = AttackDamageCalculationType.RANDOM_X_ATK
            self.mass_attack = False
            self.attack_attribute = AttackAttribute(self.args[0])
            self.minimum_multiplier = self.args[1] / 100
            self.maximum_multiplier = self.args[2] / 100
            self.suicide_hp_remaining = self.args[3] / 100

        if self.internal_skill_type == 85:
            self.damage_calculation_type = AttackDamageCalculationType.RANDOM_X_ATK
            self.mass_attack = True
            self.attack_attribute = AttackAttribute(self.args[0])
            self.minimum_multiplier = self.args[1] / 100
            self.maximum_multiplier = self.args[2] / 100
            self.suicide_hp_remaining = self.args[3] / 100

        if self.internal_skill_type == 86:
            self.damage_calculation_type = AttackDamageCalculationType.FIXED_DAMAGE
            self.mass_attack = False
            self.attack_attribute = AttackAttribute(self.args[0])
            self.fixed_damage = self.args[1]
            # TODO debug self.args[2] unused?
            self.suicide_hp_remaining = self.args[3] / 100

        if self.internal_skill_type == 87:
            self.damage_calculation_type = AttackDamageCalculationType.FIXED_DAMAGE
            self.mass_attack = True
            self.attack_attribute = AttackAttribute(self.args[0])
            self.fixed_damage = self.args[1]
            # TODO debug self.args[2] unused?
            self.suicide_hp_remaining = self.args[3] / 100

        if self.internal_skill_type == 110:
            self.damage_calculation_type = AttackDamageCalculationType.GRUDGE_X_ATK
            self.mass_attack = self.args[0] == 0
            self.attack_attribute = AttackAttribute(self.args[1])
            self.minimum_multiplier = self.args[2] / 100
            self.maximum_multiplier = self.args[3] / 100

        if self.internal_skill_type == 115:
            self.damage_calculation_type = AttackDamageCalculationType.X_ATK
            self.mass_attack = False
            self.attack_attribute = AttackAttribute(self.args[0])
            self.minimum_multiplier = self.args[1] / 100
            self.maximum_multiplier = self.args[1] / 100
            self.drain_multiplier = self.args[2] / 100

        if self.internal_skill_type == 143:
            self.damage_calculation_type = AttackDamageCalculationType.X_TEAM_HP
            self.mass_attack = True
            self.minimum_multiplier = self.args[0] / 100
            self.maximum_multiplier = self.args[0] / 100
            self.attack_attribute = AttackAttribute(self.args[1])

        if self.internal_skill_type == 144:
            self.damage_calculation_type = AttackDamageCalculationType.X_TEAM_ATK
            self.x_team_atk_attributes = tuple(AttackAttribute(a) for a in binary_to_list(self.args[0]))
            self.minimum_multiplier = self.args[1] / 100
            self.maximum_multiplier = self.args[1] / 100
            self.mass_attack = self.args[2] == 0
            self.attack_attribute = AttackAttribute(self.args[3])

    def args_to_json(self):
        return {
            'damage_calculation_type': self.damage_calculation_type.value,
            'mass_attack': self.mass_attack,
            'x_team_atk_attributes': self.x_team_atk_attributes,
            'attack_attribute': self.attack_attribute.value,
            'target_attribute': self.target_attribute.value,
            'fixed_damage': self.fixed_damage,
            'minimum_multiplier': self.minimum_multiplier,
            'maximum_multiplier': self.maximum_multiplier,
            'suicide_hp_remaining': self.suicide_hp_remaining,
            'drain_multiplier': self.drain_multiplier,
        }

    def localize(self):
        return f"" # TODO
        
    @property
    def active_skill_type(self):
        return 'attack'

    # Interface methods
    def is_suicide(self) -> bool:
        return self.suicide_hp_remaining < 1.0

    def get_suicide_percentage(self) -> float:
        return self.suicide_hp_remaining


# Register the active skill
SkillLoader._register_active_skill_class(AttackAS)