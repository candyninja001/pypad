from . import LeaderSkill
from ..skill_loader import SkillLoader
from ..region import Region

class EggDropRateLS(LeaderSkill):
    _handle_types = {53}

    def parse_args(self):
        self.multiplier = self.args[0] / 100
            
    def args_to_json(self):
        return {
            'multiplier': self.multiplier
        }

    def localize(self):
        return f"" # TODO
        
    @property
    def leader_skill_type(self):
        return 'egg_drop_rate'


# Register the active skill
SkillLoader._register_leader_skill_class(EggDropRateLS)