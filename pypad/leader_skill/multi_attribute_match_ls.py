from . import LeaderSkill
from ..skill_loader import SkillLoader
from ..region import Region
from ..orb_attribute import OrbAttribute
from ..common import list_of_binary_to_list

class MultiAttributeMatchLS(LeaderSkill):
    _handle_types = {124,164,171}

    def parse_args(self):
        self.attributes = tuple()
        self.minimum_orbs = 0
        self.minimum_atk_multiplier = 1.0
        self.minimum_rcv_multiplier = 1.0
        self.minimum_damage_reduction = 0.0
        self.bonus_atk_multiplier = 0.0
        self.bonus_rcv_mutliplier = 0.0
        self.bonus_damage_reduction = 0.0
        self.maximum_orbs = 0

        if self.internal_skill_type == 124:
            self.attributes = tuple(OrbAttribute(o) for o in list_of_binary_to_list(self.args[0:5]))
            self.minimum_orbs = self.args[5]
            self.minimum_atk_multiplier = self.args[6] / 100
            self.bonus_atk_multiplier = self.args[7] / 100
            self.maximum_orbs = len(self.attributes)

        if self.internal_skill_type == 164:
            self.attributes = tuple(OrbAttribute(o) for o in list_of_binary_to_list(self.args[0:4]))
            self.minimum_orbs = self.args[4]
            self.minimum_atk_multiplier = self.args[5] / 100
            self.minimum_rcv_multiplier = self.args[6] / 100
            self.bonus_atk_multiplier = self.args[7] / 100
            self.bonus_rcv_multiplier = self.args[7] / 100
            self.maximum_orbs = len(self.attributes)

        if self.internal_skill_type == 171:
            self.attributes = tuple(OrbAttribute(o) for o in list_of_binary_to_list(self.args[0:4]))
            self.minimum_orbs = self.args[4]
            self.minimum_atk_multiplier = self.args[5] / 100
            self.minimum_damage_reduction = self.args[6] / 100
            self.maximum_orbs = len(self.attributes)
            
    def args_to_json(self):
        return {
            'attributes': [o.value for o in self.attributes],
            'minimum_orbs': self.minimum_orbs,
            'minimum_atk_multiplier': self.minimum_atk_multiplier,
            'minimum_rcv_multiplier': self.minimum_rcv_multiplier,
            'minimum_damage_reduction': self.minimum_damage_reduction,
            'bonus_atk_multiplier': self.bonus_atk_multiplier,
            'bonus_rcv_multiplier': self.bonus_rcv_multiplier,
            'bonus_damage_reduction': self.bonus_damage_reduction,
            'maximum_orbs': self.maximum_orbs,
        }

    def localize(self):
        return f"" # TODO
        
    @property
    def leader_skill_type(self):
        return 'multi_attribute_match'


# Register the active skill
SkillLoader._register_leader_skill_class(MultiAttributeMatchLS)