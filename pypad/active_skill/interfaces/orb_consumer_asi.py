import abc
from ...orb_attribute import OrbAttribute


# Interface for active skills that remove specific orb types (e.g. orb change)
class OrbConsumerASI(abc.ABC):
    @abc.abstractmethod
    def does_orb_consumer_remove_orb_attribute(self, orb_attribute: OrbAttribute) -> bool:
        pass