from . import LeaderSkill
from ..skill_loader import SkillLoader
from ..region import Region
from ..attack_attribute import all_attr
from ..orb_attribute import OrbAttribute
from ..common import binary_to_list

class AttributeMatchLS(LeaderSkill):
    _handle_types = {61,165,170,194}

    def parse_args(self):
        self.attributes = tuple()

        self.minimum_attributes = 0
        self.minimum_atk_multiplier = 1.0
        self.minimum_rcv_multiplier = 1.0
        self.minimum_damage_reduction = 0.0
        self.minimum_extra_combo = 0
        
        self.bonus_atk_multiplier = 0.0
        self.bonus_rcv_multiplier = 0.0
        self.bonus_damage_reduction = 0.0
        self.bonus_extra_combo = 0

        self.maximum_attributes = 0
        self.reduction_attributes = all_attr

        if self.internal_skill_type == 61:
            self.attributes = tuple(OrbAttribute(o) for o in binary_to_list(self.args[0]))
            self.minimum_attributes = self.args[1]
            self.minimum_atk_multiplier = self.args[2] / 100
            self.bonus_atk_multiplier = self.args[3] / 100
            self.maximum_attributes = min(self.args[1] + self.args[4], len(self.attributes))

        elif self.internal_skill_type == 165:
            self.attributes = tuple(OrbAttribute(o) for o in binary_to_list(self.args[0]))
            self.minimum_attributes = self.args[1]
            self.minimum_atk_multiplier = self.args[2] / 100
            self.minimum_damage_reduction = self.args[3] / 100
            self.bonus_atk_multiplier = self.args[4] / 100
            self.bonus_rcv_multiplier = self.args[5] / 100
            self.maximum_attributes = min(self.args[1] + self.args[6], len(self.attributes))

        elif self.internal_skill_type == 165:
            self.attributes = tuple(OrbAttribute(o) for o in binary_to_list(self.args[0]))
            self.minimum_attributes = self.args[1]
            self.minimum_atk_multiplier = self.args[2] / 100
            self.minimum_rcv_multiplier = self.args[3] / 100
            self.maximum_attributes = self.args[1]

        elif self.internal_skill_type == 165:
            self.attributes = tuple(OrbAttribute(o) for o in binary_to_list(self.args[0]))
            self.minimum_attributes = self.args[1]
            self.minimum_atk_multiplier = self.args[2] / 100
            self.minimum_extra_combo = self.args[3]
            self.maximum_attributes = self.args[1]


    def args_to_json(self):
        return {
            'attributes': [o.value for o in self.attributes],
            'minimum_attributes': self.minimum_attributes,
            'minimum_atk_multiplier': self.minimum_atk_multiplier,
            'minimum_rcv_multiplier': self.minimum_rcv_multiplier,
            'minimum_damage_reduction': self.minimum_damage_reduction,
            'minimum_extra_combo': self.minimum_extra_combo,
            'bonus_atk_multiplier': self.bonus_atk_multiplier,
            'bonus_rcv_multiplier': self.bonus_rcv_multiplier,
            'bonus_damage_reduction': self.bonus_damage_reduction,
            'bonus_extra_combo': self.bonus_extra_combo,
            'maximum_attributes': self.maximum_attributes,
        }

    def localize(self):
        return f"" # TODO
        
    @property
    def leader_skill_type(self):
        return 'attribute_match'


# Register the active skill
SkillLoader._register_leader_skill_class(AttributeMatchLS)