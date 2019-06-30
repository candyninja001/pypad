from . import ActiveSkill
from ..skill_loader import SkillLoader
from ..attack_attribute import AttackAttribute

class AttributeATKAndRCVBoostAS(ActiveSkill):
    _handle_types = {50,90}

    def parse_args(self):

        if self.internal_skill_type == 50:
            self.duration = self.args[0]
            if self.args[1] != 5:
                self.attributes = (AttackAttribute(self.args[1]),)
                self.recovery = False
            else:
                self.attributes = tuple()
                self.recovery = True
            self.multiplier = self.args[2]

        elif self.internal_skill_type == 90:
            self.duration = self.args[0]
            self.attributes = [AttackAttribute(a) for a in self.args[1:3] if a != 5]
            self.recovery = (5 in self.args[1:3])
            self.multiplier = self.args[3]

    def args_to_json(self):
        return {
            'duration': self.duration,
            'atk_attributes': [a.value for a in self.attributes],
            'recovery': self.recovery,
            'multiplier': self.multiplier,
        }

    def localize(self):
        return '' # TODO
        
    @property
    def active_skill_type(self):
        return 'attribute_atk_and_rcv_boost'


# Register the active skill
SkillLoader._register_active_skill_class(AttributeATKAndRCVBoostAS)