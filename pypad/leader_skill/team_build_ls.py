from . import LeaderSkill
from ..skill_loader import SkillLoader
from ..region import Region
from ..common import optional_multiplier

class TeamBuildLS(LeaderSkill):
    _handle_types = {125}

    def parse_args(self):
        self.monster_ids = tuple(m for m in self.args[0:5])
        self.hp_multiplier = optional_multiplier(self.args[5])
        self.atk_multiplier = optional_multiplier(self.args[6])
        self.rcv_multiplier = optional_multiplier(self.args[7])
            
    def args_to_json(self):
        return {
            'monster_ids': [m for m in self.monster_ids],
            'hp_multiplier': self.hp_multiplier,
            'atk_multiplier': self.atk_multiplier,
            'rcv_multiplier': self.rcv_multiplier,
        }

    def localize(self):
        "All attributes xStats when all cards are on the team"
        return f"" # TODO
        
    @property
    def leader_skill_type(self):
        return 'team_build'


# Register the active skill
SkillLoader._register_leader_skill_class(TeamBuildLS)