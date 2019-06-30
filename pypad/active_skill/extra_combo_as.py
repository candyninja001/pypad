from . import ActiveSkill
from ..skill_loader import SkillLoader
from ..region import Region

class ExtraComboAS(ActiveSkill):
    _handle_types = {160}

    def parse_args(self):
        self.duration = self.args[0]
        self.combos = self.args[1]

    def args_to_json(self):
        return {
            'duration': self.duration,
            'combos': self.combos,
        }

    def localize(self):
        localization = 'For 1 turn,' if self.duration == 1 else f'For {self.duration} turns,'
        localization += ' +1 combo' if self.combos == 1 else f' +{self.combos} combos'
        return localization
        
    @property
    def active_skill_type(self):
        return 'extra_combo'


# Register the active skill
SkillLoader._register_active_skill_class(ExtraComboAS)