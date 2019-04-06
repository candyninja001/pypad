from ..region import Region
from ..read_only_property import read_only_property

class ActiveSkill:
    _loaded = False

    @classmethod
    def _get_skill_types(cls) -> [int]:
        return []

    def __init__(self, active_skill_id: int, name: str, description: str, internal_skill_type: int, max_skill: int, base_cooldown: int, args):
        self.id = active_skill_id
        self.name = name
        self.description = description
        self._internal_skill_type = internal_skill_type
        self.max_skill = max_skill
        self.base_cooldown = base_cooldown

        self._loaded = True

    def to_json(self, localization_region=None) -> dict:
        skill_json = {
            'id': self.id,
            'name': self.name,
            'card_description': self.description,
            'type': self.active_skill_type,
            'max_skill': self.max_skill,
            'base_cooldown': self.base_cooldown,
            'args': {},
        }
        if localization_region != None and type(localization_region) == Region:
            skill_json['localization'] = self.localize(localization_region)
        return skill_json

    def localize(self, region=Region.NA) -> str:
        return ''

    def get_cooldown_at_skill_level(self, skill_level):
        return self.base_cooldown - max(1, min(self.max_skill, skill_level)) + 1
        
    @read_only_property
    def active_skill_type(self):
        return 'active_skill_type_' + str(self._internal_skill_type)

    @read_only_property
    def max_skill_cooldown(self):
        return self.base_cooldown - self.max_skill + 1

    # protect the read only attributes
    def __setattr__(self, name, value):
        if (self._loaded):
            raise Exception('Cannot set attributes of ActiveSkill')
        self.__dict__[name] = value