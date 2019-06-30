from . import ActiveSkill 
from ..skill_loader import SkillLoader

class UnlockOrbsAS(ActiveSkill):
    _handle_types = {172}

    def parse_args(self):
        pass

    def args_to_json(self):
        return {}

    def localize(self):
        return 'Unlock all orbs'
        
    @property
    def active_skill_type(self):
        return 'unlock_orbs'


# Register the active skill
SkillLoader._register_active_skill_class(UnlockOrbsAS)