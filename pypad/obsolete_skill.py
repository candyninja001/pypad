from .active_skill import ActiveSkill
from .leader_skill import LeaderSkill
from .dev import Dev

class ObsoleteSkill(ActiveSkill, LeaderSkill):
    _handle_types = {89}

    def parse_args(self):
        if self.internal_skill_type == 89:
            if self.args[0] != 100:
                Dev.log('Unexpected value in t_89, skill might be used now')

    def args_to_json(self):
        return {}

    def localize(self):
        return ''
        
    @property
    def active_skill_type(self):
        return 'obsolete'


# Register the obsolete skill
#   Moved registration to SkillLoader to prevent circular imports
#SkillLoader._register_active_skill_class(ObsoleteSkill)
#SkillLoader._register_leader_skill_class(ObsoleteSkill)