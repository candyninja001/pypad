from . import LeaderSkill
from ..skill_loader import SkillLoader
from ..region import Region
from ..attack_attribute import AttackAttribute, all_attr
from ..monster_type import MonsterType
from ..common import binary_to_list, optional_multiplier

class ThresholdStatsDualLS(LeaderSkill):
    _handle_types = {139,183}

    def parse_args(self):
        self.for_attributes = tuple(AttackAttribute(a) for a in binary_to_list(self.args[0]))
        self.for_types = tuple(MonsterType(t) for t in binary_to_list(self.args[1]))

        self.threshold_1 = 0.0
        self.above_1 = False
        self.atk_multiplier_1 = 1.0
        self.rcv_multiplier_1 = 1.0
        self.damage_reduction_1 = 0.0

        self.threshold_2 = 0.0
        self.above_2 = False
        self.atk_multiplier_2 = 1.0
        self.rcv_multiplier_2 = 1.0
        self.damage_reduction_2 = 0.0

        if self.internal_skill_type == 139:
            self.threshold_1 = self.args[2] / 100
            self.above_1 = not bool(self.args[3])
            self.atk_multiplier_1 = self.args[4] / 100

            self.threshold_2 = self.args[5] / 100
            self.above_2 = not bool(self.args[6])
            self.atk_multiplier_2 = self.args[7] / 100
            
        elif self.internal_skill_type == 183:
            self.threshold_1 = self.args[2] / 100
            self.above_1 = True
            self.atk_multiplier_1 = optional_multiplier(self.args[3])
            self.damage_reduction_1 = self.args[4] / 100

            self.threshold_2 = self.args[5] / 100
            self.above_2 = False
            self.atk_multiplier_2 = optional_multiplier(self.args[6])
            self.rcv_multiplier_2 = optional_multiplier(self.args[7])

    def args_to_json(self):
        return {
            'for_attributes': [a.value for a in self.for_attributes],
            'for_types': [t.value for t in self.for_types],
            'threshold_1': self.threshold_1,
            'above_1': self.above_1,
            'atk_multiplier_1': self.atk_multiplier_1,
            'rcv_multiplier_1': self.rcv_multiplier_1,
            'damage_reduction_1': self.damage_reduction_1,
            'threshold_2': self.threshold_2,
            'above_2': self.above_2,
            'atk_multiplier_2': self.atk_multiplier_2,
            'rcv_multiplier_2': self.rcv_multiplier_2,
            'damage_reduction_2': self.damage_reduction_2,
        }

    def localize(self):
        return f"" # TODO
        
    @property
    def leader_skill_type(self):
        return 'threshold_stats_dual'


# Register the active skill
SkillLoader._register_leader_skill_class(ThresholdStatsDualLS)