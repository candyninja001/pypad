from . import ActiveSkill
from ..skill_loader import SkillLoader
from .interfaces.multi_skill_asi import MultiSkillASI
from ..region import Region
from ..game import Game

class CombineActiveSkillsAS(ActiveSkill, MultiSkillASI):
    _handle_types = {116}

    def parse_args(self):
        self.active_skill_ids = tuple(i for i in self.args[:])

    def args_to_json(self):
        return {
            'skill_ids': [as_id for as_id in self.active_skill_ids]
        }

    def localize(self):
        # TODO localize for multihit lasers
        return ';\n'.join(Game(self._region).active_skill_book[as_id].localize() for as_id in self.active_skill_ids)
        
    @property
    def active_skill_type(self):
        return 'combine_active_skills'

    # Interface methods
    def get_sub_skills(self):
        return self.active_skill_ids


# Register the active skill
SkillLoader._register_active_skill_class(CombineActiveSkillsAS)