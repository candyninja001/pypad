from . import LeaderSkill
from ..skill_loader import SkillLoader
from ..region import Region
from ..common import optional_multiplier

class HeartCrossLS(LeaderSkill):
    _handle_types = {151}

    def parse_args(self):
        self.atk_multiplier = optional_multiplier(self.args[0])
        self.rcv_multiplier = optional_multiplier(self.args[1])
        self.damage_reuction = self.args[2] / 100
            
    def args_to_json(self):
        return {
            'atk_multiplier': self.atk_multiplier,
            'rcv_multiplier': self.rcv_multiplier,
            'damage_reuction': self.damage_reuction,
        }

    def localize(self):
        return f"" # TODO
        
    @property
    def leader_skill_type(self):
        return 'heart_cross'


# Register the active skill
SkillLoader._register_leader_skill_class(HeartCrossLS)