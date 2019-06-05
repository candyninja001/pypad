from . import ActiveSkill
from ..skill_loader import SkillLoader
from ..region import Region
from ..orb_attribute import OrbAttribute
from ..board_pattern import BoardPattern

class CreateOrbPatternAS(ActiveSkill):
    _handle_types = {176}

    def parse_args(self):
        self.pattern = BoardPattern(self.args[0:5])
        self.orb = OrbAttribute(self.args[5])

    def args_to_json(self):
        return {
            'pattern': self.pattern.to_json(),
            'orb': self.orb.value,
        }

    def localize(self):
        return f"" #TODO localize
        
    @property
    def active_skill_type(self):
        return 'create_orb_pattern'


# Register the active skill
SkillLoader._register_active_skill_class(CreateOrbPatternAS)