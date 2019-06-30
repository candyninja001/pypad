from . import LeaderSkill
from ..skill_loader import SkillLoader
from ..region import Region
from ..collab import Collab
from ..common import optional_multiplier

class CollabStatsLS(LeaderSkill):
    _handle_types = {175}

    def parse_args(self):
        self.collab = Collab(self.args[0])
        self.hp_multiplier = optional_multiplier(self.args[3])
        self.atk_multiplier = optional_multiplier(self.args[4])
        self.rcv_multiplier = optional_multiplier(self.args[5])
            
    def args_to_json(self):
        return {
            'collab': self.collab.value,
            'hp_multiplier': self.hp_multiplier,
            'atk_multiplier': self.atk_multiplier,
            'rcv_multiplier': self.rcv_multiplier,
        }

    def localize(self):
        return f"xStats when all subs are from collab" # TODO
        
    @property
    def leader_skill_type(self):
        return 'collab_stats'


# Register the active skill
SkillLoader._register_leader_skill_class(CollabStatsLS)