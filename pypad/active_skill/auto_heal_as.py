from . import ActiveSkill
from ..skill_loader import SkillLoader
from ..region import Region

class AutoHealAS(ActiveSkill):
    _handle_types = {179}

    def parse_args(self):
        self.duration = self.args[0]
        print(f'[AutoHealAS] skill [{self.id}] args: {repr(self.args)}')
        # TODO this skill is not JUST autoheal

    def args_to_json(self):
        return {
        }

    def localize(self):
        return f"" # TODO localize
        
    @property
    def active_skill_type(self):
        return 'auto_heal'


# Register the active skill
SkillLoader._register_active_skill_class(AutoHealAS)