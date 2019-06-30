from . import ActiveSkill
from ..skill_loader import SkillLoader
from ..region import Region
from ..attack_attribute import AttackAttribute

class EnemyAttributeChangeAS(ActiveSkill):
    _handle_types = {153}

    def parse_args(self):
        self.attribute = AttackAttribute(self.args[0])

    def args_to_json(self):
        return {
            'attribute': self.attribute,
        }

    def localize(self):
        return f"Change enemies' attributes to {self.attribute.name.capitalize}"
        
    @property
    def active_skill_type(self):
        return 'enemy_attribute_change'


# Register the active skill
SkillLoader._register_active_skill_class(EnemyAttributeChangeAS)