from . import LeaderSkill
from ..skill_loader import SkillLoader
from ..region import Region
from ..attack_attribute import AttackAttribute
from ..monster_type import MonsterType
from ..common import binary_to_list, optional_multiplier

class MultiplayerStatsLS(LeaderSkill):
    _handle_types = {155}

    def parse_args(self):
        self.for_attributes = tuple(AttackAttribute(a) for a in binary_to_list(self.args[0]))
        self.for_types = tuple(MonsterType(t) for t in binary_to_list(self.args[1]))
        self.hp_multiplier = optional_multiplier(self.args[2])
        self.atk_multiplier = optional_multiplier(self.args[3])
        self.rcv_multiplier = optional_multiplier(self.args[4])
            
    def args_to_json(self):
        return {
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
        return 'multiplayer_stats'


# Register the active skill
SkillLoader._register_leader_skill_class(MultiplayerStatsLS)