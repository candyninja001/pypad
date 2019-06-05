from . import LeaderSkill
from ..skill_loader import SkillLoader
from ..region import Region

class ComboMatchExactLS(LeaderSkill):
    _handle_types = {101}

    def parse_args(self):
        self.combos = self.args[0]
        self.atk_multiplier = self.args[1] / 100
            
    def args_to_json(self):
        return {
            'combos': self.combos,
            'atk_multiplier': self.atk_multiplier,
        }

    def localize(self):
        return f"" # TODO
        
    @property
    def leader_skill_type(self):
        return 'combo_match_exact'


# Register the active skill
SkillLoader._register_leader_skill_class(ComboMatchExactLS)