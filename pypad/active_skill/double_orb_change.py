from . import ActiveSkill
from ..skill_loader import SkillLoader
from ..region import Region
from ..orb_attribute import OrbAttribute

class DoubleOrbChangeAS(ActiveSkill):
    _handle_types = {20}

    def parse_args(self):
        self.from_orb_1 = OrbAttribute(self.args[0])
        self.to_orb_1 = OrbAttribute(self.args[1])
        self.from_orb_2 = OrbAttribute(self.args[2])
        self.to_orb_2 = OrbAttribute(self.args[3])

    def args_to_json(self):
        return {
            'from_1': self.from_orb_1.value,
            'to_1': self.to_orb_1.value,
            'from_2': self.from_orb_2.value,
            'to_2': self.to_orb_2.value,
        }

    def localize(self):
        return f"Change {self.from_orb_1.name.capitalize()} to {self.to_orb_1.name.capitalize()} and {self.from_orb_2.name.capitalize()} to {self.to_orb_2.name.capitalize()}"
        
    @property
    def active_skill_type(self):
        return 'double_orb_change'


# Register the active skill
SkillLoader._register_active_skill_class(DoubleOrbChangeAS)