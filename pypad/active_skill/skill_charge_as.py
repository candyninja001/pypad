from . import ActiveSkill 
from ..skill_loader import SkillLoader
from ..region import Region

class SkillChargeAS(ActiveSkill):
    _handle_types = {146}

    def parse_args(self):
        self.charge_minimum = self.args[0]
        self.charge_maximum = self.args[1]

    def args_to_json(self):
        return {
            'minimum': self.charge_minimum,
            'maximum': self.charge_maximum,
        }

    def localize(self):
        localization = "Other cards' active skill cooldowns reduced by " + self.charge_minimum
        if self.charge_maximum != self.charge_minimum:
            localization += ' to ' + self.charge_maximum
        localization += ' turn' if self.charge_maximum == 1 else ' turns'
        return localization
        
    @property
    def active_skill_type(self):
        return 'skill_charge'

# Register the active skill
SkillLoader._register_active_skill_class(SkillChargeAS)