from ..parser.common import defaultlist
from ..parser.parse_status import ParseStatus
from ..region import Region
from ..data import get_raw_file
from . import ActiveSkill
from .unknown_active_skill import UnknownActiveSkill

class ActiveSkills:
    _active_skill_classes = {}
    _version = 1220

    @classmethod
    def _add_active_skill_class(cls, active_skill_class: ActiveSkill):
        internal_types = active_skill_class._get_skill_types()
        for internal_type in internal_types:
            if internal_type not in cls._active_skill_classes:
                cls._active_skill_classes[internal_type] = []
            cls._active_skill_classes[internal_type].append(active_skill_class)

    def __init__(self, region=Region.NA, dev=False):
        self._region = region
        raw_skill_json = get_raw_file('download_skill_data.json', self._region)
        self._raw_version = raw_skill_json['v']
        if dev:
            if self._raw_version != self._version:
                print(f'Mismatched parsing version and raw data version for active skills ({self._version} vs {self._raw_version})')
        
        self._active_skills = {}
        for i,raw_skill in enumerate(raw_skill_json['skill']):
            # only parse active skills
            if raw_skill[3] != 0 or raw_skill[4] != 0:
                skill_args = {}
                skill_args['active_skill_id'] = i
                skill_args['name'] = raw_skill[0]
                skill_args['description'] = raw_skill[1]
                skill_args['internal_skill_type'] = raw_skill[2]
                skill_args['max_skill'] = raw_skill[3]
                skill_args['base_cooldown'] = raw_skill[4]
                skill_args['args'] = defaultlist(int, raw_skill[6:])

                if dev:
                    status = self._add_active_skill(**skill_args)
                    if status == ParseStatus.UNKNOWN:
                        print(f'Found unknown active skill [{i}]')
                else:
                    self._add_active_skill(**skill_args)

    def _add_active_skill(self, active_skill_id: int, name: str, description: str, internal_skill_type: int, max_skill: int, base_cooldown: int, args) -> ParseStatus:
        if internal_skill_type not in self._active_skill_classes:
            self._active_skills[active_skill_id] = UnknownActiveSkill(active_skill_id, name, description, internal_skill_type, max_skill, base_cooldown, args)
            return ParseStatus.UNKNOWN
        self._active_skill_classes[internal_skill_type](active_skill_id, name, description, internal_skill_type, max_skill, base_cooldown, args)
        return ParseStatus.GOOD

    def get_active_skill(self, skill_id: int) -> ActiveSkill:
        if skill_id not in self._active_skills:
            return None
        return self._active_skills[skill_id]