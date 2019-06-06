import abc
from ...orb_attribute import OrbAttribute


# Interface for active skills that create specific orb types (whether board change, orb change, orb spawn, etc)
class OrbGeneratorASI(abc.ABC):
    @abc.abstractmethod
    def does_orb_generator_create_orb_attribute(self, orb_attribute: OrbAttribute) -> bool:
        pass