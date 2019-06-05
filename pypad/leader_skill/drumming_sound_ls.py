from . import LeaderSkill
from ..skill_loader import SkillLoader
from ..region import Region

class DrummingSoundLS(LeaderSkill):
    _handle_types = {33}

    @classmethod
    def handles(cls, raw_skill) -> bool:
        return True

    def parse_args(self):
        pass
            
    def args_to_json(self):
        return {
        }

    def localize(self):
        return f"Drumming sound when moving orbs"
        
    @property
    def leader_skill_type(self):
        return 'drumming_sound'


# Register the active skill
SkillLoader._register_leader_skill_class(DrummingSoundLS)