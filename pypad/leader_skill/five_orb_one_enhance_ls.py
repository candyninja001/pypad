from . import LeaderSkill
from ..skill_loader import SkillLoader
from ..region import Region

class FiveOrbOneEnhanceLS(LeaderSkill):
    _handle_types = {150}

    def parse_args(self):
        self.atk_multiplier = self.args[1] / 100
            
    def args_to_json(self):
        return {
            'atk_multiplier': self.atk_multiplier,
        }

    
    def localize(self):
        return f"{self.atk_multiplier}x ATK per attribute when matching 5 connected Orbs with 1 enhanced Orb"
        
    @property
    def leader_skill_type(self):
        return 'five_orb_one_enhance'


# Register the active skill
SkillLoader._register_leader_skill_class(FiveOrbOneEnhanceLS)