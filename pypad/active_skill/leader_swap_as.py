from . import ActiveSkill 
from ..skill_loader import SkillLoader
from ..region import Region

class LeaderSwapAS(ActiveSkill):
    _handle_types = {93}

    def parse_args(self):
        pass

    def args_to_json(self):
        return {}

    def localize(self):
        return "Swap places with the current leader, or move back to position as sub"
        
    @property
    def active_skill_type(self):
        return 'leader_swap'


# Register the active skill
SkillLoader._register_active_skill_class(LeaderSwapAS)