from ..parser.common import defaultlist
from ..parser.parse_status import ParseStatus
from ..region import Region
from ..data import get_raw_file
from . import LeaderSkill
from .unknown_leader_skill import UnknownLeaderSkill

class LeaderSkills:
    _leader_skill_classes = {}
    _version = 1220

    @classmethod
    def _add_leader_skill_class(cls, leader_skill_class: LeaderSkill):
        internal_types = leader_skill_class._get_skill_types()
        for internal_type in internal_types:
            if internal_type not in cls._leader_skill_classes:
                cls._leader_skill_classes[internal_type] = []
            cls._leader_skill_classes[internal_type].append(leader_skill_class)

    def __init__(self, region=Region.NA, dev=False):
        self._region = region
        raw_skill_json = get_raw_file('download_skill_data.json', self._region)
        self._raw_version = raw_skill_json['v']
        if dev:
            if self._raw_version != self._version:
                print(f'Mismatched parsing version and raw data version for leader skills ({self._version} vs {self._raw_version})')
        
        self._leader_skills = {}
        for i,raw_skill in enumerate(raw_skill_json['skill']):
            # only parse leader skills
            if raw_skill[3] == 0 and raw_skill[4] == 0:
                skill_args = {}
                skill_args['leader_skill_id'] = i
                skill_args['name'] = raw_skill[0]
                skill_args['description'] = raw_skill[1]
                skill_args['internal_skill_type'] = raw_skill[2]
                skill_args['args'] = defaultlist(int, raw_skill[6:])

                if dev:
                    status = self._add_leader_skill(**skill_args)
                    if status == ParseStatus.UNKNOWN:
                        print(f'Found unknown leader skill [{i}]')
                else:
                    self._add_leader_skill(**skill_args)

    def _add_leader_skill(self, leader_skill_id: int, name: str, description: str, internal_skill_type: int, args) -> ParseStatus:
        if internal_skill_type not in self._leader_skill_classes:
            self._leader_skills[leader_skill_id] = UnknownLeaderSkill(leader_skill_id, name, description, internal_skill_type, args)
            return ParseStatus.UNKNOWN
        self._leader_skill_classes[internal_skill_type](leader_skill_id, name, description, internal_skill_type, args)
        return ParseStatus.GOOD

    def get_leader_skill(self, skill_id: int) -> LeaderSkill:
        if skill_id not in self._leader_skills:
            return None
        return self._leader_skills[skill_id]