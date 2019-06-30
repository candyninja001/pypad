from . import LeaderSkill
from ..skill_loader import SkillLoader
from ..region import Region
from ..attack_attribute import AttackAttribute, all_attr
from ..monster_type import MonsterType
from ..common import binary_to_list, optional_multiplier

class ThresholdStatsAboveLS(LeaderSkill):
    _handle_types = {43,44,96,97,123,131}

    def parse_args(self):
        self.threshold = self.args[0] / 100

        self.for_attributes = all_attr
        self.for_types = tuple()
        self.atk_multiplier = 1.0
        self.rcv_multiplier = 1.0
        self.reduction_attributes = all_attr
        self.damage_reduction = 0.0

        if self.internal_skill_type == 43:
            self.damage_reduction = self.args[2] / 100

        elif self.internal_skill_type == 44:
            self.atk_multiplier = self.args[3] if 1 in self.args[1:3] else 1.0
            self.rcv_multiplier = self.args[3] if 2 in self.args[1:3] else 1.0

        elif self.internal_skill_type == 96:
            self.for_attributes = (AttackAttribute(self.args[1]),)
            self.atk_multiplier = self.args[4] if 1 in self.args[2:4] else 1.0
            self.rcv_multiplier = self.args[4] if 2 in self.args[2:4] else 1.0

        elif self.internal_skill_type == 97:
            self.for_attributes = tuple()
            self.for_types = (MonsterType(self.args[1]),)
            self.atk_multiplier = self.args[4] if 1 in self.args[2:4] else 1.0
            self.rcv_multiplier = self.args[4] if 2 in self.args[2:4] else 1.0

        elif self.internal_skill_type == 123:
            self.for_attributes = tuple(AttackAttribute(a) for a in binary_to_list(self.args[1]))
            self.for_types = tuple(MonsterType(t) for t in binary_to_list(self.args[2]))
            self.atk_multiplier = optional_multiplier(self.args[3])
            self.rcv_multiplier = optional_multiplier(self.args[4])

        elif self.internal_skill_type == 131:
            self.for_attributes = tuple(AttackAttribute(a) for a in binary_to_list(self.args[1]))
            self.for_types = tuple(MonsterType(t) for t in binary_to_list(self.args[2]))
            self.atk_multiplier = optional_multiplier(self.args[3])
            self.rcv_multiplier = optional_multiplier(self.args[4])
            self.reduction_attributes = tuple(AttackAttribute(a) for a in binary_to_list(self.args[5]))
            self.damage_reduction = self.args[6] / 100

    def args_to_json(self):
        return {
            'for_attributes': [a.value for a in self.for_attributes],
            'for_types': [t.value for t in self.for_types],
            'threshold': self.threshold,
            'atk_multiplier': self.atk_multiplier,
            'rcv_multiplier': self.rcv_multiplier,
            'reduction_attributes': [a.value for a in self.reduction_attributes],
            'damage_reduction': self.damage_reduction,
        }

    def localize(self):
        return f"" # TODO
        
    @property
    def leader_skill_type(self):
        return 'threshold_stats_above'


# Register the active skill
SkillLoader._register_leader_skill_class(ThresholdStatsAboveLS)