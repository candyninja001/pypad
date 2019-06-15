from . import ActiveSkill 
from ..skill_loader import SkillLoader

class ReduceUnmatchableDebuffAS(ActiveSkill):
    _handle_types = {196}

    @classmethod
    def handles(self, raw_skill):
        return True

    def parse_args(self):
        self.turns = self.args[0]

    def args_to_json(self):
        return {
            'turns': self.turns,
        }

    def localize(self):
        return f"Reduce unmatchable orb state by {'1 turn' if self.turns == 1 else f'{self.turns} turns'}"
        
    @property
    def active_skill_type(self):
        return 'reduce_unmatchable_debuff'


# Register the active skill
SkillLoader._register_active_skill_class(ReduceUnmatchableDebuffAS)