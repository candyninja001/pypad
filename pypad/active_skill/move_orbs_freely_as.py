from . import ActiveSkill 
from ..skill_loader import SkillLoader
from ..region import Region

class MoveOrbsFreelyAS(ActiveSkill):
    _handle_types = {5}

    def parse_args(self):
        self.seconds = self.args[0]

    def args_to_json(self):
        return {
            'seconds': self.seconds,
        }

    def localize(self):
        return f"Move orbs freely for {self.seconds} seconds"
        
    @property
    def active_skill_type(self):
        return 'move_orbs_freely'


# Register the active skill
SkillLoader._register_active_skill_class(MoveOrbsFreelyAS)