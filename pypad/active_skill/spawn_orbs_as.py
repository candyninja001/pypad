from . import ActiveSkill 
from .interfaces.orb_generator_asi import OrbGeneratorASI
from ..skill_loader import SkillLoader
from ..region import Region
from ..orb_attribute import OrbAttribute
from ..common import binary_to_list, iterable_to_string

class SpawnOrbsAS(ActiveSkill, OrbGeneratorASI):
    _handle_types = {141}

    def parse_args(self):
        self.amount = self.args[0]
        self.orbs = tuple(OrbAttribute(o) for o in binary_to_list(self.args[1]))
        self.excluding_orbs = tuple(OrbAttribute(o) for o in binary_to_list(self.args[2]))

    def args_to_json(self):
        return {
            'amount': self.amount,
            'orbs': [o.value for o in self.orbs],
            'excluding_orbs': [o.value for o in self.excluding_orbs],
        }

    def localize(self):
        spawn_orbs_string = iterable_to_string(orb.name.capitalize() for orb in self.orbs)
        localization = f"Create {self.amount} {spawn_orbs_string} Orbs"
        orb_difference = [o.name.capitalize() for o in self.excluding_orbs if o not in self.orbs]
        excluding_orbs_string = iterable_to_string(orb_difference)
        if len(orb_difference) > 0:
            localization += f" from non {excluding_orbs_string} Orbs"
        else:
            localization += ' at random' # TODO remove?
        return localization
        
    @property
    def active_skill_type(self):
        return 'spawn_orbs'

    # Interface methods
    def does_orb_generator_create_orb_attribute(self, orb_attribute: OrbAttribute) -> bool:
        return orb_attribute in self.orbs


# Register the active skill
SkillLoader._register_active_skill_class(SpawnOrbsAS)