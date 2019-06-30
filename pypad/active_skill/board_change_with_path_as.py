from . import ActiveSkill
from .interfaces.orb_generator_asi import OrbGeneratorASI
from ..skill_loader import SkillLoader
from ..region import Region
from ..orb_attribute import OrbAttribute

class BoardChangeWithPathAS(ActiveSkill):
    _handle_types = {189}

    def parse_args(self):
        self.unlock = True
        self.orbs = (OrbAttribute.FIRE,OrbAttribute.WATER,OrbAttribute.WOOD,OrbAttribute.LIGHT)
        self.path_combo_count = 3

    def args_to_json(self):
        return {
            'unlock': self.unlock,
            'orbs': [o.value for o in self.orbs],
            'path_combo_count': self.path_combo_count,
        }

    def localize(self):
        return f"" # TODO localize
        
    @property
    def active_skill_type(self):
        return 'board_change_with_path'

    # Interface methods
    def does_orb_generator_create_orb_attribute(self, orb_attribute: OrbAttribute) -> bool:
        return orb_attribute in self.orbs


# Register the active skill
SkillLoader._register_active_skill_class(BoardChangeWithPathAS)