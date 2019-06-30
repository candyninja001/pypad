from . import LeaderSkill
from ..skill_loader import SkillLoader
from ..region import Region

class HealTPALS(LeaderSkill):
    _handle_types = {149}

    def parse_args(self):
        self.rcv_multiplier = self.args[0] / 100
            
    def args_to_json(self):
        return {
            'rcv_multiplier': self.rcv_multiplier,
        }

    def localize(self):
        return f"All attributes {self.rcv_multiplier}x RCV when matching 4 connected Heal Orbs"
        
    @property
    def leader_skill_type(self):
        return 'heal_tpa'


# Register the active skill
SkillLoader._register_leader_skill_class(HealTPALS)