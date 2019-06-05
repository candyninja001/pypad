from . import LeaderSkill
from ..skill_loader import SkillLoader
from ..region import Region
from ..orb_attribute import OrbAttribute

class ColorCross:
    def __init__(self, attribute, atk_multiplier):
        self.attribute = OrbAttribute(attribute)
        self.atk_multiplier = atk_multiplier / 100
    
    def to_json(self):
        return {
            'attribute': self.attribute.value,
            'atk_multiplier': self.atk_multiplier,
        }

class ColorCrossLS(LeaderSkill):
    _handle_types = {157}

    def parse_args(self):
        self.crosses = tuple(ColorCross(a,m) for a,m in zip(self.args[::2],self.args[1::2]))
            
    def args_to_json(self):
        return {
            'crosses': [cross.to_json() for cross in self.crosses]
        }

    def localize(self):
        return f"" # TODO
        
    @property
    def leader_skill_type(self):
        return 'color_cross'


# Register the active skill
SkillLoader._register_leader_skill_class(ColorCrossLS)