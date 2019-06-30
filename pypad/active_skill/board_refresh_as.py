from . import ActiveSkill
from ..skill_loader import SkillLoader
from ..region import Region

class BoardRefreshAS(ActiveSkill):
    _handle_types = {10}

    def parse_args(self):
        pass

    def args_to_json(self):
        return {}

    def localize(self):
        return f"Replace the board"
        
    @property
    def active_skill_type(self):
        return 'board_refresh'


# Register the active skill
SkillLoader._register_active_skill_class(BoardRefreshAS)