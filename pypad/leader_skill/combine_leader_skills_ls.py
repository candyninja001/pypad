from . import LeaderSkill
from ..skill_loader import SkillLoader
from .interfaces.multi_skill_lsi import MultiSkillLSI
from ..region import Region
from ..game import Game

class CombineLeaderSkillsAS(LeaderSkill, MultiSkillLSI):
    _handle_types = {138}

    def parse_args(self):
        self.leader_skill_ids = tuple(i for i in self.args[:])

    def args_to_json(self):
        return {
            'skill_ids': [as_id for as_id in self.leader_skill_ids]
        }

    def localize(self):
        return ';\n'.join(Game(self._region).leader_skill_book[ls_id].localize() for ls_id in self.leader_skill_ids)
        
    @property
    def leader_skill_type(self):
        return 'combine_leader_skills'

    # Interface methods
    def get_sub_skills(self):
        return self.leader_skill_ids


# Register the leader skill
SkillLoader._register_leader_skill_class(CombineLeaderSkillsAS)