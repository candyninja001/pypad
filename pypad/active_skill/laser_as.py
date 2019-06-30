from . import ActiveSkill 
from ..skill_loader import SkillLoader
from ..region import Region

class LaserAS(ActiveSkill):
    _handle_types = {55,56}

    def parse_args(self):
        self.damage = self.args[0]
        self.mass_attack = self.internal_skill_type == 56

    def args_to_json(self):
        return {
            'damage': self.damage,
            'mass_attack': self.mass_attack,
        }

    def localize(self):
        return f"Deal {self.damage} damage to {'all enemies' if self.mass_attack else '1 enemy'}"
        
    @property
    def active_skill_type(self):
        return 'laser'


# Register the active skill
SkillLoader._register_active_skill_class(LaserAS)