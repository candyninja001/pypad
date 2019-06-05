from . import ActiveSkill
from ..skill_loader import SkillLoader
from ..region import Region
from ..awakening import Awakening
from ..common import iterable_to_string

class AwakeningShieldAS(ActiveSkill):
    _handle_types = {156}

    @classmethod
    def handles(cls, raw_skill):
        return raw_skill[10] == 3

    def parse_args(self):
        self.duration = self.args[0]
        self.awakenings = tuple(Awakening(a) for a in self.args[1:4])
        self.reduction_per = self.args[5] / 100

    def args_to_json(self):
        return {
            'duration': self.duration,
            'awakenings': [a.value for a in self.awakenings],
            'reduction_per': self.reduction_per,
        }

    def localize(self):
        return f"" # TODO localize
        
    @property
    def active_skill_type(self):
        return 'awakening_shield'


# Register the active skill
SkillLoader._register_active_skill_class(AwakeningShieldAS)