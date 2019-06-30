from . import LeaderSkill
from ..skill_loader import SkillLoader
from ..region import Region
from ..attack_attribute import AttackAttribute, all_attr
from ..monster_type import MonsterType
from ..common import binary_to_list, optional_multiplier

class SkillUsedLS(LeaderSkill):
    _handle_types = {100,133}

    def parse_args(self):
        self.for_attributes = all_attr
        self.for_types = tuple()
        self.atk_multiplier = 1.0
        self.rcv_multiplier = 1.0

        if self.internal_skill_type == 100:
            self.atk_multiplier = self.args[2] / 100 if 1 in self.args[0:2] else 1.0
            self.rcv_multiplier = self.args[2] / 100 if 2 in self.args[0:2] else 1.0

        elif self.internal_skill_type == 133:
            self.for_attributes = tuple(AttackAttribute(a) for a in binary_to_list(self.args[0]))
            self.for_types = tuple(MonsterType(t) for t in binary_to_list(self.args[1]))
            self.atk_multiplier = optional_multiplier(self.args[2])
            self.rcv_multiplier = optional_multiplier(self.args[3])

    def args_to_json(self):
        return {
            'for_attributes': [a.value for a in self.for_attributes],
            'for_types': [t.value for t in self.for_types],
            'atk_multiplier': self.atk_multiplier,
            'rcv_multiplier': self.rcv_multiplier,
        }

    def localize(self):
        return f"" # TODO
        
    @property
    def leader_skill_type(self):
        return 'skill_used'


# Register the active skill
SkillLoader._register_leader_skill_class(SkillUsedLS)