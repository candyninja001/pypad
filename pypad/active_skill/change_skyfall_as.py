from . import ActiveSkill
from ..skill_loader import SkillLoader
from ..region import Region
from ..common import binary_to_list, iterable_to_string
from ..orb_attribute import OrbAttribute

class ChangeSkyfallAS(ActiveSkill):
    _handle_types = {126}

    def parse_args(self):
        self.orbs = tuple(OrbAttribute(o) for o in binary_to_list(self.args[0]))
        self.duration = self.args[1]
        if self.args[1] != self.args[2]:
            print(f'[Warning] unexpected behavior in ChangeSkyfallAS [{self.id}]')
        self.rate_increase = self.args[3] / 100

    def args_to_json(self):
        return {
            'orbs': [o.value for o in self.orbs],
            'duration': self.duration,
            'rate_increase': self.rate_increase
        }

    def localize(self):
        orbs_string = iterable_to_string(orb.name.capitalize() for orb in self.orbs)
        
        localization = 'For 1 turn,' if self.duration == 1 else f'For {self.duration} turns,'
        localization += f' {orbs_string} Orbs are each {self.rate_increase*100}% more likely to appear'
        if len(self.orbs) > 1:
            localization += f' ({(len(self.orbs)*self.rate_increase)*100}% total)'
        return localization
        
    @property
    def active_skill_type(self):
        return 'change_skyfall'


# Register the active skill
SkillLoader._register_active_skill_class(ChangeSkyfallAS)