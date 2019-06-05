from . import ActiveSkill 
from ..skill_loader import SkillLoader
from ..region import Region
from ..monster_type import MonsterType

class TypeATKBoostAS(ActiveSkill):
    _handle_types = {88,92}

    def parse_args(self):
        
        if self.internal_skill_type == 88:
            self.duration = self.args[0]
            self.types = (MonsterType(self.args[1]),)
            self.multiplier = self.args[2] / 100

        elif self.internal_skill_type == 92:
            self.duration = self.args[0]
            self.types = tuple(MonsterType(t) for t in self.args[1:3])
            self.multiplier = self.args[3] / 100

    def args_to_json(self):
        return {
            'duration': self.duration,
            'types': [t.value for t in self.types],
            'multiplier': self.multiplier,
        }

    def localize(self):
        localization = 'For 1 turn,' if self.duration == 1 else f'For {self.duration} turns,'
        localization += f' {self.multiplier}x ATK for'
        if len(self.types) == 1:
            localization += f' {self.types[0].name.capitalize()} type'
        else:
            localization += f' {self.types[0].name.capitalize()} and {self.types[1].name.capitalize()} types'
        return localization
        
    @property
    def active_skill_type(self):
        return 'type_atk_boost'


# Register the active skill
SkillLoader._register_active_skill_class(TypeATKBoostAS)