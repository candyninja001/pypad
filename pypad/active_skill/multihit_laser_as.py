from . import ActiveSkill 
from ..skill_loader import SkillLoader
from ..region import Region

class MultihitLaserAS(ActiveSkill):
    _handle_types = {188}

    def parse_args(self):
        self.damage = self.args[0]
        self.mass_attack = False

    def args_to_json(self):
        return {
            'damage': self.damage,
            'mass_attack': self.mass_attack,
        }

    def localize(self):
        return f"Deal {self.damage} damage to 1 enemy"
        
    @property
    def active_skill_type(self):
        return 'mutlihit_laser'


# Register the active skill
SkillLoader._register_active_skill_class(MultihitLaserAS)