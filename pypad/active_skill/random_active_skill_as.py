from . import ActiveSkill 
from ..skill_loader import SkillLoader
from .interfaces.multi_skill_asi import MultiSkillASI
from ..region import Region
from ..game import Game

class RandomActiveSkillAS(ActiveSkill, MultiSkillASI):
    _handle_types = {118}

    def parse_args(self):
        self.active_skill_ids = tuple(i for i in self.args[:])

    def args_to_json(self):
        return {
            'skill_ids': [as_id for as_id in self.active_skill_ids]
        }

    def localize(self):
        return 'Randomly use one of the following skills:\n'+';\n'.join(Game(self._region).active_skill_book[as_id].localize() for as_id in self.active_skill_ids)
        
    @property
    def active_skill_type(self):
        return 'random_active_skill'

    # Interface methods
    def get_sub_skills(self):
        return self.active_skill_ids


# Register the active skill
SkillLoader._register_active_skill_class(RandomActiveSkillAS)