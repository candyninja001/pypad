from . import ActiveSkill

class UnknownActiveSkill(ActiveSkill):
    def __init__(self, active_skill_id: int, name: str, description: str, internal_skill_type: int, max_skill: int, base_cooldown: int, args):
        super(UnknownActiveSkill, self).__init__(active_skill_id, name, description, internal_skill_type, max_skill, base_cooldown, args)
        self._args = list(args)

    def get_active_skill_type(self) -> str:
        return 'unknown_active_skill_type_' + str(self._internal_skill_type)

    def to_json(self) -> dict:
        skill_json = super(UnknownActiveSkill, self).to_json()
        skill_json['args'] = {'arg_'+str(i):self._args[i] for i in range(len(self._args))}
        return skill_json