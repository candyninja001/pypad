from . import ActiveSkill 
from .interfaces.orb_consumer_asi import OrbConsumerASI
from .interfaces.orb_generator_asi import OrbGeneratorASI
from ..skill_loader import SkillLoader
from ..region import Region
from ..orb_attribute import OrbAttribute
from ..common import binary_to_list, iterable_to_string

class RandomOrbChangeAS(ActiveSkill, OrbGeneratorASI, OrbConsumerASI):
    _handle_types = {154}

    def parse_args(self):
        self.from_orbs = tuple(OrbAttribute(o) for o in binary_to_list(self.args[0]))
        self.to_orbs = tuple(OrbAttribute(o) for o in binary_to_list(self.args[1]))

    def args_to_json(self):
        return {
            'from_orbs': [o.value for o in self.from_orbs],
            'to_orbs': [o.value for o in self.to_orbs],
        }

    def localize(self):
        from_orbs_string = iterable_to_string(o.name.capitalize() for o in self.from_orbs)
        to_orbs_string = iterable_to_string(o.name.capitalize() for o in self.to_orbs)
        return f"Change {from_orbs_string} orbs to {to_orbs_string} orbs"
        
    @property
    def active_skill_type(self):
        return 'random_orb_change'

    # Interface methods
    def does_orb_generator_create_orb_attribute(self, orb_attribute: OrbAttribute) -> bool:
        return orb_attribute in self.to_orbs
    
    def does_orb_consumer_remove_orb_attribute(self, orb_attribute: OrbAttribute) -> bool:
        return orb_attribute in self.from_orbs


# Register the active skill
SkillLoader._register_active_skill_class(RandomOrbChangeAS)