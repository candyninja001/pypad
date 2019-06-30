from . import ActiveSkill 
from ..skill_loader import SkillLoader
from ..region import Region

class MoveTimePercentageAS(ActiveSkill):
    _handle_types = {132}

    @classmethod
    def handles(cls, raw_skill):
        return raw_skill[8] != 0

    def parse_args(self):
        self.duration = self.args[0]
        self.percentage_increase = self.args[2] / 100

    def args_to_json(self):
        return {
            'duration': self.duration,
            'percentage_increase': self.percentage_increase,
        }

    def localize(self):
        localization = 'For 1 turn,' if self.duration == 1 else f'For {self.duration} turns,'
        if self.percentage_increase < 0:
            localization += f' decrease orb move time by {-self.percentage_increase}%'
        else:
            localization += f' increase orb move time by {self.percentage_increase}%'
        return localization
        
    @property
    def active_skill_type(self):
        return 'move_time_percentage'


# Register the active skill
SkillLoader._register_active_skill_class(MoveTimePercentageAS)