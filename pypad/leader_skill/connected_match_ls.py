from . import LeaderSkill
from ..skill_loader import SkillLoader
from ..region import Region
from ..orb_attribute import OrbAttribute
from ..common import binary_to_list, optional_multiplier

class ConnectedMatchLS(LeaderSkill):
    _handle_types = {109,119,159,167,182}

    def parse_args(self):
        self.attributes = tuple(OrbAttribute(o) for o in binary_to_list(self.args[0]))
        self.minimum_orbs = self.args[1]

        self.minimum_atk_multiplier = 1.0
        self.minimum_rcv_multiplier = 1.0
        self.minimum_damage_reduction = 0.0
        self.bonus_atk_multiplier = 0.0
        self.bonus_rcv_multiplier = 0.0
        self.bonus_damage_reduction = 0.0
        self.maximum_orbs = self.args[1]

        if self.internal_skill_type == 109:
            self.minimum_atk_multiplier = self.args[2] / 100

        if self.internal_skill_type == 119: # TODO verify
            self.minimum_atk_multiplier = self.args[2] / 100
            self.bonus_atk_multiplier = self.args[3] / 100
            self.maximum_orbs = self.args[4]

        if self.internal_skill_type == 159: # TODO verify
            self.minimum_atk_multiplier = self.args[2] / 100
            self.bonus_atk_multiplier = self.args[3] / 100
            self.maximum_orbs = self.args[4]

        if self.internal_skill_type == 167:
            self.minimum_atk_multiplier = optional_multiplier(self.args[2])
            self.minimum_rcv_multiplier = optional_multiplier(self.args[3])
            self.bonus_atk_multiplier = self.args[4] / 100
            self.bonus_rcv_multiplier = self.args[5] / 100
            self.maximum_orbs = self.args[6]

        if self.internal_skill_type == 182:
            self.minimum_atk_multiplier = self.args[2] / 100
            self.minimum_damage_reduction = self.args[3] / 100

            
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
        return 'connected_match'


# Register the active skill
SkillLoader._register_leader_skill_class(ConnectedMatchLS)