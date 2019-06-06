from . import ActiveSkill 
from .interfaces.suicide_asi import SuicideASI
from ..skill_loader import SkillLoader

class SuicideAS(ActiveSkill, SuicideASI):
    _handle_types = {195}

    def parse_args(self):
        self.remaining_hp_percent = self.args[0] / 100

    def args_to_json(self):
        return {
            'remaining_hp_percent': self.remaining_hp_percent,
        }

    def localize(self):
        return f"HP is reduced {'to 1' if self.remaining_hp_percent == 0 else f'by {(1.0-self.remaining_hp_percent)*100}%'}"
        
    @property
    def active_skill_type(self):
        return 'suicide'

    # Interface methods
    def is_suicide(self) -> bool:
        return self.remaining_hp_percent < 1.0

    def get_suicide_percentage(self) -> float:
        return self.remaining_hp_percent


# Register the active skill
SkillLoader._register_active_skill_class(SuicideAS)