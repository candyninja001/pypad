from . import ActiveSkill
from ..skill_loader import SkillLoader
from ..region import Region

class DefenseReductionAS(ActiveSkill):
    _handle_types = {19}

    def parse_args(self):
        self.duration = self.args[0]
        self.reduction = self.args[1] / 100

    def args_to_json(self):
        return {
            'duration': self.duration,
            'reduction': self.reduction,
        }

    def localize(self):
        return f"Reduce enemies' defense by {self.reduction*100}%"
        
    @property
    def active_skill_type(self):
        return 'defense_reduction'


# Register the active skill
SkillLoader._register_active_skill_class(DefenseReductionAS)