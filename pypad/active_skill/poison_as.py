from . import ActiveSkill 
from ..skill_loader import SkillLoader

class PoisonAS(ActiveSkill):
    _handle_types = {4}

    def parse_args(self):
        self.multiplier = self.args[0] / 100

    def args_to_json(self):
        return {
            'multiplier': self.multiplier,
        }

    def localize(self):
        return f"Poison all enemies for {self.multiplier}x ATK damage"
        
    @property
    def active_skill_type(self):
        return 'poison'


# Register the active skill
SkillLoader._register_active_skill_class(PoisonAS)