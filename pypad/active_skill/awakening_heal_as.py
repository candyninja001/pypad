from . import ActiveSkill
from ..skill_loader import SkillLoader
from ..region import Region
from ..awakening import Awakening
from ..common import iterable_to_string

class AwakeningHealAS(ActiveSkill):
    _handle_types = {156}

    @classmethod
    def handles(cls, raw_skill):
        return raw_skill[10] == 1

    def parse_args(self):
        # TODO verify behavior
        self.awakenings = tuple(Awakening(a) for a in self.args[1:4])
        self.hp_per = self.args[5]

    def args_to_json(self):
        return {
            'awakenings': [a.value for a in self.awakenings],
            'hp_per': self.hp_per,
        }

    def localize(self):
        return f"" # TODO localize
        
    @property
    def active_skill_type(self):
        return 'awakening_heal'


# Register the active skill
SkillLoader._register_active_skill_class(AwakeningHealAS)