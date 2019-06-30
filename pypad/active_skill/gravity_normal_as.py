from . import ActiveSkill 
from ..skill_loader import SkillLoader
from ..region import Region

class GravityNormalAS(ActiveSkill):
    _handle_types = {6}

    def parse_args(self):
        self.percentage = self.args[0] / 100

    def args_to_json(self):
        return {
            'percentage_hp': self.percentage,
        }

    def localize(self):
        return f"Deal damage equal to {self.percentage*100}% enemies' current HP"
        
    @property
    def active_skill_type(self):
        return 'gravity_normal'


# Register the active skill
SkillLoader._register_active_skill_class(GravityNormalAS)