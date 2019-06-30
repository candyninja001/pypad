from . import LeaderSkill
from ..skill_loader import SkillLoader
from ..region import Region
from ..attack_attribute import AttackAttribute,all_attr
from ..common import binary_to_list, optional_multiplier

class ComboMatchLS(LeaderSkill):
    _handle_types = {66,98,103,104,166,169}

    def parse_args(self):
        self.for_attributes = all_attr

        self.minimum_combos = 0
        self.minimum_atk_multiplier = 1.0
        self.minimum_rcv_multiplier = 1.0
        self.minimum_damage_reduction = 0.0
        
        self.bonus_atk_multiplier = 0.0
        self.bonus_rcv_multiplier = 0.0
        self.bonus_damage_reduction = 0.0

        self.maximum_combos = 0
        self.reduction_attributes = all_attr

        if self.internal_skill_type == 66:
            self.minimum_combos = self.args[0]
            self.minimum_atk_multiplier = self.args[1] / 100
            self.maximum_combos = self.args[0]

        elif self.internal_skill_type == 98:
            self.minimum_combos = self.args[0]
            self.minimum_atk_multiplier = self.args[1] / 100
            self.bonus_atk_multiplier = self.args[2] / 100
            self.maximum_combos = self.args[3]

        elif self.internal_skill_type == 103:
            self.minimum_combos = self.args[0]
            self.minimum_atk_multiplier = self.args[3] / 100 if 1 in self.args[1:3] else 1.0
            self.minimum_rcv_multiplier = self.args[3] / 100 if 2 in self.args[1:3] else 1.0
            self.maximum_combos = self.args[0]

        elif self.internal_skill_type == 104:
            self.minimum_combos = self.args[0]
            self.for_attributes = tuple(AttackAttribute(a) for a in binary_to_list(self.args[1]))
            self.minimum_atk_multiplier = self.args[4] / 100 if 1 in self.args[2:4] else 1.0
            self.minimum_rcv_multiplier = self.args[4] / 100 if 2 in self.args[2:4] else 1.0
            self.maximum_combos = self.args[0]

        elif self.internal_skill_type == 166:
            self.minimum_combos = self.args[0]
            self.minimum_atk_multiplier = optional_multiplier(self.args[1])
            self.minimum_rcv_multiplier = optional_multiplier(self.args[2])
            self.bonus_atk_multiplier = self.args[3] / 100
            self.bonus_rcv_multiplier = self.args[4] / 100
            self.maximum_combos = self.args[5]

        elif self.internal_skill_type == 166:
            self.minimum_combos = self.args[0]
            self.minimum_atk_multiplier = self.args[1] / 100
            self.minimum_damage_reduction = self.args[2] / 100
            self.maximum_combos = self.args[0]


    def args_to_json(self):
        return {
            'for_attributes': [o.value for o in self.for_attributes],
            'minimum_combos': self.minimum_combos,
            'minimum_atk_multiplier': self.minimum_atk_multiplier,
            'minimum_rcv_multiplier': self.minimum_rcv_multiplier,
            'minimum_damage_reduction': self.minimum_damage_reduction,
            'bonus_atk_multiplier': self.bonus_atk_multiplier,
            'bonus_rcv_multiplier': self.bonus_rcv_multiplier,
            'bonus_damage_reduction': self.bonus_damage_reduction,
            'maximum_combos': self.maximum_combos,
        }

    def localize(self):
        return f"" # TODO
        
    @property
    def leader_skill_type(self):
        return 'combo_match'


# Register the active skill
SkillLoader._register_leader_skill_class(ComboMatchLS)