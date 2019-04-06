from ..region import Region
from ..read_only_property import read_only_property

class LeaderSkill:
    _loaded = False

    @classmethod
    def _get_skill_types(cls) -> [int]:
        return []

    def __init__(self, leader_skill_id: int, name: str, description: str, internal_skill_type: int, args):
        self.id = leader_skill_id
        self.name = name
        self.description = description
        self._internal_skill_type = internal_skill_type

        self._loaded = True

    def to_json(self, localization_region=None) -> dict:
        skill_json = {
            'id': self.id,
            'name': self.name,
            'card_description': self.description,
            'type': self.leader_skill_type,
            'args': {},
        }
        if localization_region != None and type(localization_region) == Region:
            skill_json['localization'] = self.localize(localization_region)
        return skill_json

    def localize(self, region=Region.NA) -> str:
        return ''
        
    @read_only_property
    def leader_skill_type(self):
        return 'leader_skill_type_' + str(self._internal_skill_type)

    # protect the read only attributes
    def __setattr__(self, name, value):
        if (self._loaded):
            raise Exception('Cannot set attributes of LeaderSkill')
        self.__dict__[name] = value