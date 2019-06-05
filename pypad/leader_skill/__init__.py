from ..region import Region
from ..parser.common import defaultlist
from collections import defaultdict

from .interfaces.multi_skill_lsi import MultiSkillLSI


class LeaderSkill:
    _handle_types = set()

    @classmethod
    def handles(cls, raw_skill) -> bool:
        return len(raw_skill) > 6

    def __init__(self, skill_id, raw_skill, region):
        self._region = region
        self.id = skill_id
        self.name = raw_skill[0]
        self.description = raw_skill[1]
        self.internal_skill_type = raw_skill[2]
        self.args = defaultlist(int, raw_skill[6:])
        self.parse_args()

    def parse_args(self):
        pass

    def to_json(self, localize=False) -> dict:
        skill_json = {
            'id': self.id,
            'name': self.name,
            'card_description': self.description,
            'type': self.leader_skill_type,
            'args': self.args_to_json(),
        }
        if localize:
            skill_json['localization'] = self.localize()
        return skill_json

    def args_to_json(self) -> dict:
        return {'arg_'+str(i):self.args[i] for i in range(len(self.args))}

    def localize(self) -> str:
        return ''
        
    @property
    def leader_skill_type(self):
        return 'leader_skill_type_' + str(self.internal_skill_type)


class LeaderSkillBook:
    def __init__(self):
        self._skills = {}
        self._sub_skill_uses = defaultdict(set)

    def _register(self, leader_skill):
        if leader_skill != None:
            self._skills[leader_skill.id] = leader_skill
            if isinstance(leader_skill, MultiSkillLSI):
                for sub_skill_id in leader_skill.get_sub_skills():
                    self._sub_skill_uses[sub_skill_id].add(leader_skill.id)

    def __contains__(self, leader_skill_id) -> bool:
        return leader_skill_id in self._skills
    
    def __getitem__(self, leader_skill_id) -> LeaderSkill:
        return self._skills[leader_skill_id]

    def __iter__(self):
        return iter(self._skills.values())

    def __len__(self):
        return len(self._skills)

    # Returns the set of multi-skills including sub_skill_id as a sub-skill
    def sub_skill_instances(self, sub_skill_id):
        return {self._skills[as_id] for as_id in self._sub_skill_uses[sub_skill_id]}

    def to_json(self):
        return {str(skill_id):skill.to_json() for skill_id,skill in self._skills.items()}
