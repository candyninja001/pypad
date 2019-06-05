from . import LeaderSkill
from ..skill_loader import SkillLoader
from ..region import Region

class ResolveLS(LeaderSkill):
    _handle_types = {14}

    def parse_args(self):
        self.threshold = self.args[0] / 100
        # TODO investigate self.args[1]
            
    def args_to_json(self):
        return {
            'threshold': self.threshold,
        }

    def localize(self):
        return f"" # TODO
        
    @property
    def leader_skill_type(self):
        return 'resolve'


# Register the active skill
SkillLoader._register_leader_skill_class(ResolveLS)