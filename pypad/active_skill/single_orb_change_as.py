from . import ActiveSkill 
from .interfaces.orb_consumer_asi import OrbConsumerASI
from .interfaces.orb_generator_asi import OrbGeneratorASI
from ..skill_loader import SkillLoader
from ..region import Region
from ..orb_attribute import OrbAttribute

class SingleOrbChangeAS(ActiveSkill, OrbGeneratorASI, OrbConsumerASI):
    _handle_types = {9}

    def parse_args(self):
        self.from_orb = OrbAttribute(self.args[0])
        self.to_orb = OrbAttribute(self.args[1])

    def args_to_json(self):
        return {
            'from': self.from_orb.value,
            'to': self.to_orb.value,
        }

    def localize(self):
        return f"Change {self.from_orb.name.capitalize()} Orbs to {self.to_orb.name.capitalize()} Orbs"
        
    @property
    def active_skill_type(self):
        return 'single_orb_change'

    # Interface methods
    def does_orb_generator_create_orb_attribute(self, orb_attribute: OrbAttribute) -> bool:
        return orb_attribute == self.to_orb
    
    def does_orb_consumer_remove_orb_attribute(self, orb_attribute: OrbAttribute) -> bool:
        return orb_attribute == self.from_orb


# Register the active skill
SkillLoader._register_active_skill_class(SingleOrbChangeAS)