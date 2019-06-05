from . import LeaderSkill
from ..skill_loader import SkillLoader
from ..region import Region
from ..attack_attribute import AttackAttribute
from ..monster_type import MonsterType
from ..common import binary_to_list, optional_multiplier

class PassiveStatsDualLS(LeaderSkill):
    _handle_types = {136,137}

    def parse_args(self):
        self.for_attributes_1 = tuple()
        self.for_types_1 = tuple()
        self.hp_multiplier_1 = optional_multiplier(self.args[1])
        self.atk_multiplier_1 = optional_multiplier(self.args[2])
        self.rcv_multiplier_1 = optional_multiplier(self.args[3])
        
        self.for_attributes_2 = tuple()
        self.for_types_2 = tuple()
        self.hp_multiplier_2 = optional_multiplier(self.args[5])
        self.atk_multiplier_2 = optional_multiplier(self.args[6])
        self.rcv_multiplier_2 = optional_multiplier(self.args[7])

        if self.internal_skill_type == 136:
            self.for_attributes_1 = tuple(AttackAttribute(a) for a in binary_to_list(self.args[0]))
            self.for_attributes_2 = tuple(AttackAttribute(a) for a in binary_to_list(self.args[4]))
        
        if self.internal_skill_type == 137:
            self.for_type_1 = tuple(MonsterType(t) for t in binary_to_list(self.args[0]))
            self.for_type_2 = tuple(MonsterType(t) for t in binary_to_list(self.args[4]))

    def args_to_json(self):
        return {
            'for_attributes_1': [a.value for a in self.for_attributes_1],
            'for_types_1': [t.value for t in self.for_types_1],
            'hp_multiplier_1': self.hp_multiplier_1,
            'atk_multiplier_1': self.atk_multiplier_1,
            'rcv_multiplier_1': self.rcv_multiplier_1,
            'for_attributes_2': [a.value for a in self.for_attributes_2],
            'for_types_2': [t.value for t in self.for_types_2],
            'hp_multiplier_2': self.hp_multiplier_2,
            'atk_multiplier_2': self.atk_multiplier_2,
            'rcv_multiplier_2': self.rcv_multiplier_2,
        }

    def localize(self):
        return f"" # TODO
        
    @property
    def leader_skill_type(self):
        return 'passive_stats_dual'


# Register the active skill
SkillLoader._register_leader_skill_class(PassiveStatsDualLS)