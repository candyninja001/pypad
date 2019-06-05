from ..region import Region
from ..parser.common import defaultlist
from collections import defaultdict

from .interfaces.multi_skill_asi import MultiSkillASI


class ActiveSkill:
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
        self.max_skill = raw_skill[3]
        self.base_cooldown = raw_skill[4]
        self.args = defaultlist(int, raw_skill[6:])
        self.parse_args()

    def parse_args(self):
        pass

    def to_json(self, localize=False) -> dict:
        skill_json = {
            'id': self.id,
            'name': self.name,
            'card_description': self.description,
            'type': self.active_skill_type,
            'max_skill': self.max_skill,
            'base_cooldown': self.base_cooldown,
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
    def active_skill_type(self):
        return 'active_skill_type_' + str(self.internal_skill_type)

    @property
    def max_skill_cooldown(self):
        return self.base_cooldown - self.max_skill + 1


class ActiveSkillBook:
    def __init__(self):
        self._skills = {}
        self._sub_skill_uses = defaultdict(set)

    def _register(self, active_skill):
        if active_skill != None:
            self._skills[active_skill.id] = active_skill
            if isinstance(active_skill, MultiSkillASI):
                for sub_skill_id in active_skill.get_sub_skills():
                    self._sub_skill_uses[sub_skill_id].add(active_skill.id)

    def __contains__(self, active_skill_id) -> bool:
        return active_skill_id in self._skills
    
    def __getitem__(self, active_skill_id) -> ActiveSkill:
        return self._skills[active_skill_id]

    def __iter__(self):
        return iter(self._skills.values())

    def __len__(self):
        return len(self._skills)

    # Returns the set of multi-skills including sub_skill_id as a sub-skill
    def sub_skill_instances(self, sub_skill_id):
        return {self._skills[as_id] for as_id in self._sub_skill_uses[sub_skill_id]}

    def to_json(self):
        return {str(skill_id):skill.to_json() for skill_id,skill in self._skills.items()}
