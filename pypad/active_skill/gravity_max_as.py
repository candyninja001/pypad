from . import ActiveSkill
from ..skill_loader import SkillLoader
from ..region import Region

class GravityMaxAS(ActiveSkill):
    _handle_types = {161}

    def parse_args(self):
        self.percentage_max_hp = self.args[0] / 100

    def args_to_json(self):
        return {
            'percentage_max_hp': self.percentage_max_hp,
        }

    def localize(self):
        return f"Deal damage equal to {self.percentage_max_hp*100}% enemies' maximum HP"
        
    @property
    def active_skill_type(self):
        return 'gravity_max'


# Register the active skill
SkillLoader._register_active_skill_class(GravityMaxAS)