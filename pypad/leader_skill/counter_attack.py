from . import LeaderSkill
from ..skill_loader import SkillLoader
from ..region import Region
from ..attack_attribute import AttackAttribute

class CounterAttackLS(LeaderSkill):
    _handle_types = {41}

    def parse_args(self):
        self.chance = self.args[0] / 100
        self.multiplier = self.args[1] / 100
        self.attribute = AttackAttribute(self.args[2])
            
    def args_to_json(self):
        return {
            'chance': self.chance,
            'multiplier': self.multiplier,
            'attribute': self.attribute.value,
        }

    def localize(self):
        return f"" # TODO
        
    @property
    def leader_skill_type(self):
        return 'counter_attack'


# Register the active skill
SkillLoader._register_leader_skill_class(CounterAttackLS)