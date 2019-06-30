from . import LeaderSkill
from ..skill_loader import SkillLoader
from ..region import Region
from ..attack_attribute import AttackAttribute
from ..monster_type import MonsterType
from ..common import binary_to_list, optional_multiplier

class BonusMoveTimeLS(LeaderSkill):
    _handle_types = {15,185}

    def parse_args(self):
        self.fixed_time = self.args[0] / 100
        self.for_attributes = tuple()
        self.for_types = tuple()
        self.hp_multiplier = 1.0
        self.atk_multiplier = 1.0
        self.rcv_multiplier = 1.0

        if self.internal_skill_type == 185:
            self.for_attributes = tuple(AttackAttribute(a) for a in binary_to_list(self.args[1]))
            self.for_types = tuple(MonsterType(t) for t in binary_to_list(self.args[2]))
            self.hp_multiplier = optional_multiplier(self.args[3])
            self.atk_multiplier = optional_multiplier(self.args[4])
            self.rcv_multiplier = optional_multiplier(self.args[5])
            
    def args_to_json(self):
        return {
            'fixed_time': self.fixed_time,
            'for_attributes': [a.value for a in self.for_attributes],
            'for_types': [t.value for t in self.for_types],
            'hp_multiplier': self.hp_multiplier,
            'atk_multiplier': self.atk_multiplier,
            'rcv_multiplier': self.rcv_multiplier,
        }

    def localize(self):
        return f"" # TODO
        
    @property
    def leader_skill_type(self):
        return 'bonus_move_time'


# Register the active skill
SkillLoader._register_leader_skill_class(BonusMoveTimeLS)