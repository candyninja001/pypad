from ..region import Region
from ..read_only_property import read_only_property

class ActiveSkill:
    @classmethod
    def _get_skill_types(cls) -> [int]:
        return []

    def __init__(self, active_skill_id: int, name: str, description: str, internal_skill_type: int, max_skill: int, base_cooldown: int, args):
        self._id = active_skill_id
        self._name = name
        self._description = description
        self._internal_skill_type = internal_skill_type
        self._max_skill = max_skill
        self._base_cooldown = base_cooldown

    def to_json(self, localization_region=None) -> dict:
        skill_json = {
            'id': self._id,
            'name': self._name,
            'card_description': self._description,
            'type': self.active_skill_type,
            'max_skill': self._max_skill,
            'base_cooldown': self._base_cooldown,
            'args': {},
        }
        if localization_region != None and type(localization_region) == Region:
            skill_json['localization'] = self.localize(localization_region)
        return skill_json

    def localize(self, region=Region.NA) -> str:
        return ''

    def simulate(self, dungeon_run: 'DungeonRun'):
        raise NotImplementedError

    @read_only_property
    def id(self):
        return self._id

    @read_only_property
    def description(self):
        return self._description

    @read_only_property
    def internal_skill_type(self):
        return self._internal_skill_type
        
    @read_only_property
    def active_skill_type(self):
        return 'active_skill_type_' + str(self._internal_skill_type)

    @read_only_property
    def max_skill(self):
        return self._max_skill

    @read_only_property
    def base_cooldown(self):
        return self._base_cooldown

    @read_only_property
    def max_skill_cooldown(self):
        return self._base_cooldown - self._max_skill + 1