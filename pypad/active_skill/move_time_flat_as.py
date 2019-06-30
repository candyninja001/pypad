from . import ActiveSkill 
from ..skill_loader import SkillLoader
from ..region import Region

class MoveTimeFlatAS(ActiveSkill):
    _handle_types = {132}

    @classmethod
    def handles(cls, raw_skill):
        return raw_skill[7] != 0

    def parse_args(self):
        self.duration = self.args[0]
        self.seconds = self.args[1] / 10

    def args_to_json(self):
        return {
            'duration': self.duration,
            'seconds': self.seconds,
        }

    def localize(self):
        localization = 'For 1 turn,' if self.duration == 1 else f'For {self.duration} turns,'
        if self.seconds < 0:
            localization += f' decrease orb move time by {-self.seconds} seconds'
        else:
            localization += f' increase orb move time by {self.seconds} seconds'
        return localization
        
    @property
    def active_skill_type(self):
        return 'move_time_flat'


# Register the active skill
SkillLoader._register_active_skill_class(MoveTimeFlatAS)