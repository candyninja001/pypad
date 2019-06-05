from . import ActiveSkill
from ..skill_loader import SkillLoader
from ..region import Region

class DelayAS(ActiveSkill):
    _handle_types = {18}

    def parse_args(self):
        self.turns = self.args[0]

    def args_to_json(self):
        return {
            'turns': self.turns
        }

    def localize(self):
        return f"Delay all enemies for {self.turns} {'turn' if self.turns == 1 else 'turns'}"
        
    @property
    def active_skill_type(self):
        return 'delay'


# Register the active skill
SkillLoader._register_active_skill_class(DelayAS)