from . import LeaderSkill
from ..skill_loader import SkillLoader
from ..region import Region

class OrbsRemainingLS(LeaderSkill):
    _handle_types = {177}

    def parse_args(self):
        self.maximum_orb_count = self.args[5]
        self.minimum_atk_multiplier = self.args[6] / 100
        self.bonus_atk_multiplier = self.args[7] / 100
            
    def args_to_json(self):
        return {
            'maximum_orb_count': self.maximum_orb_count,
            'minimum_atk_multiplier': self.minimum_atk_multiplier,
            'bonus_atk_multiplier': self.bonus_atk_multiplier,
        }

    def localize(self):
        return f"" # TODO
        
    @property
    def leader_skill_type(self):
        return 'orbs_remaining'


# Register the active skill
SkillLoader._register_leader_skill_class(OrbsRemainingLS)