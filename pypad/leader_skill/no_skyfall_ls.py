from . import LeaderSkill
from ..skill_loader import SkillLoader
from ..region import Region

class NoSkyfallLS(LeaderSkill):
    _handle_types = {163}

    @classmethod
    def handles(cls, raw_skill) -> bool:
        return True

    def parse_args(self):
        pass
            
    def args_to_json(self):
        return {
        }

    def localize(self):
        return f"No skyfall orbs"
        
    @property
    def leader_skill_type(self):
        return 'no_skyfall'


# Register the active skill
SkillLoader._register_leader_skill_class(NoSkyfallLS)