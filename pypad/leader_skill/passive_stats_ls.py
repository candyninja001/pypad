from . import LeaderSkill
from ..skill_loader import SkillLoader
from ..region import Region
from ..attack_attribute import AttackAttribute, all_attr
from ..monster_type import MonsterType
from ..common import binary_to_list, optional_multiplier

class PassiveStatsLS(LeaderSkill):
    _handle_types = {11,16,17,22,23,24,26,28,29,30,31,36,40,45,46,48,49,62,63,64,65,67,69,73,75,76,77,79,105,106,107,108,111,114,121,129}

    def parse_args(self):
        self.for_attributes = tuple()
        self.for_types = tuple()
        self.hp_multiplier = 1.0
        self.atk_multiplier = 1.0
        self.rcv_multiplier = 1.0
        self.reduction_attributes = all_attr
        self.damage_reduction = 0.0

        if self.internal_skill_type == 11:
            self.for_attributes = (AttackAttribute(self.args[0]),)
            self.atk_multiplier = self.args[1] / 100

        elif self.internal_skill_type == 16:
            self.for_attributes = all_attr
            self.damage_reduction = self.args[0] / 100

        elif self.internal_skill_type == 17:
            self.reduction_attributes = (AttackAttribute(self.args[0]),)
            self.damage_reduction = self.args[1] / 100

        elif self.internal_skill_type == 22:
            self.for_types = (MonsterType(self.args[0]),)
            self.atk_multiplier = self.args[1] / 100

        elif self.internal_skill_type == 23:
            self.for_types = (MonsterType(self.args[0]),)
            self.hp_multiplier = self.args[1] / 100

        elif self.internal_skill_type == 24:
            self.for_types = (MonsterType(self.args[0]),)
            self.rcv_multiplier = self.args[1] / 100

        elif self.internal_skill_type == 26:
            self.for_attributes = all_attr
            self.atk_multiplier = self.args[0] / 100

        elif self.internal_skill_type == 28:
            self.for_attributes = (AttackAttribute(self.args[0]),)
            self.atk_multiplier = self.args[1] / 100
            self.rcv_multiplier = self.args[1] / 100

        elif self.internal_skill_type == 29:
            self.for_attributes = (AttackAttribute(self.args[0]),)
            self.hp_multiplier = self.args[1] / 100
            self.atk_multiplier = self.args[1] / 100
            self.rcv_multiplier = self.args[1] / 100

        elif self.internal_skill_type == 30:
            self.for_types = tuple(MonsterType(t) for t in self.args[0:2])
            self.hp_multiplier = self.args[2] / 100

        elif self.internal_skill_type == 31:
            self.for_types = tuple(MonsterType(t) for t in self.args[0:2])
            self.atk_multiplier = self.args[2] / 100

        elif self.internal_skill_type == 36:
            self.reduction_attributes = tuple(AttackAttribute(a) for a in self.args[0:2])
            self.damage_reduction = self.args[2] / 100

        elif self.internal_skill_type == 40:
            self.for_attributes = tuple(AttackAttribute(a) for a in self.args[0:2])
            self.atk_multiplier = self.args[2] / 100

        elif self.internal_skill_type == 45:
            self.for_attributes = (AttackAttribute(self.args[0]),)
            self.hp_multiplier = self.args[1] / 100
            self.atk_multiplier = self.args[1] / 100

        elif self.internal_skill_type == 46:
            self.for_attributes = tuple(AttackAttribute(a) for a in self.args[0:2])
            self.hp_multiplier = self.args[2] / 100

        elif self.internal_skill_type == 48:
            self.for_attributes = (AttackAttribute(self.args[0]),)
            self.hp_multiplier = self.args[1] / 100

        elif self.internal_skill_type == 49:
            self.for_attributes = (AttackAttribute(self.args[0]),)
            self.rcv_multiplier = self.args[1] / 100

        elif self.internal_skill_type == 62:
            self.for_types = (MonsterType(self.args[0]),)
            self.hp_multiplier = self.args[1] / 100
            self.atk_multiplier = self.args[1] / 100

        elif self.internal_skill_type == 63:
            self.for_types = (MonsterType(self.args[0]),)
            self.hp_multiplier = self.args[1] / 100
            self.rcv_multiplier = self.args[1] / 100

        elif self.internal_skill_type == 64:
            self.for_types = (MonsterType(self.args[0]),)
            self.atk_multiplier = self.args[1] / 100
            self.rcv_multiplier = self.args[1] / 100

        elif self.internal_skill_type == 65:
            self.for_types = (MonsterType(self.args[0]),)
            self.hp_multiplier = self.args[1] / 100
            self.atk_multiplier = self.args[1] / 100
            self.rcv_multiplier = self.args[1] / 100

        elif self.internal_skill_type == 67:
            self.for_attributes = (AttackAttribute(self.args[0]),)
            self.hp_multiplier = self.args[1] / 100
            self.rcv_multiplier = self.args[1] / 100

        if self.internal_skill_type == 69:
            self.for_attributes = (AttackAttribute(self.args[0]),)
            self.for_types = (MonsterType(self.args[1]),)
            self.atk_multiplier = self.args[2] / 100

        elif self.internal_skill_type == 73:
            self.for_attributes = (AttackAttribute(self.args[0]),)
            self.for_types = (MonsterType(self.args[1]),)
            self.hp_multiplier = self.args[2] / 100
            self.atk_multiplier = self.args[2] / 100

        elif self.internal_skill_type == 75:
            self.for_attributes = (AttackAttribute(self.args[0]),)
            self.for_types = (MonsterType(self.args[1]),)
            self.atk_multiplier = self.args[2] / 100
            self.rcv_multiplier = self.args[2] / 100

        elif self.internal_skill_type == 76:
            self.for_attributes = (AttackAttribute(self.args[0]),)
            self.for_types = (MonsterType(self.args[1]),)
            self.hp_multiplier = self.args[2] / 100
            self.atk_multiplier = self.args[2] / 100
            self.rcv_multiplier = self.args[2] / 100

        elif self.internal_skill_type == 77:
            self.for_types = tuple(MonsterType(t) for t in self.args[0:2])
            self.hp_multiplier = self.args[2] / 100
            self.atk_multiplier = self.args[2] / 100

        elif self.internal_skill_type == 79:
            self.for_types = tuple(MonsterType(t) for t in self.args[0:2])
            self.atk_multiplier = self.args[2] / 100
            self.rcv_multiplier = self.args[2] / 100

        elif self.internal_skill_type == 105:
            self.for_attributes = all_attr
            self.atk_multiplier = self.args[1] / 100
            self.rcv_multiplier = self.args[0] / 100

        elif self.internal_skill_type == 106:
            self.for_attributes = all_attr
            self.hp_multiplier = self.args[0] / 100
            self.atk_multiplier = self.args[1] / 100

        elif self.internal_skill_type == 107:
            self.for_attributes = all_attr
            self.hp_multiplier = self.args[0] / 100

        elif self.internal_skill_type == 108:
            self.for_types = (MonsterType(self.args[1]),)
            self.hp_multiplier = self.args[0] / 100
            self.atk_multiplier = self.args[2] / 100

        elif self.internal_skill_type == 111:
            self.for_attributes = tuple(AttackAttribute(a) for a in self.args[0:2])
            self.hp_multiplier = self.args[2] / 100
            self.atk_multiplier = self.args[2] / 100

        elif self.internal_skill_type == 114:
            self.for_attributes = tuple(AttackAttribute(a) for a in self.args[0:2])
            self.hp_multiplier = self.args[2] / 100
            self.atk_multiplier = self.args[2] / 100
            self.rcv_multiplier = self.args[2] / 100

        elif self.internal_skill_type == 121:
            self.for_attributes = tuple(AttackAttribute(a) for a in binary_to_list(self.args[0]))
            self.for_types = tuple(MonsterType(t) for t in binary_to_list(self.args[1]))
            self.hp_multiplier = optional_multiplier(self.args[2])
            self.atk_multiplier = optional_multiplier(self.args[3])
            self.rcv_multiplier = optional_multiplier(self.args[4])

        elif self.internal_skill_type == 129:
            self.for_attributes = tuple(AttackAttribute(a) for a in binary_to_list(self.args[0]))
            self.for_types = tuple(MonsterType(t) for t in binary_to_list(self.args[1]))
            self.hp_multiplier = optional_multiplier(self.args[2])
            self.atk_multiplier = optional_multiplier(self.args[3])
            self.rcv_multiplier = optional_multiplier(self.args[4])
            self.reduction_attributes = tuple(AttackAttribute(a) for a in binary_to_list(self.args[5]))
            self.damage_reduction = self.args[6] / 100
            
    def args_to_json(self):
        return {
            'for_attributes': [a.value for a in self.for_attributes],
            'for_types': [t.value for t in self.for_types],
            'hp_multiplier': self.hp_multiplier,
            'atk_multiplier': self.atk_multiplier,
            'rcv_multiplier': self.rcv_multiplier,
            'reduction_attributes': [a.value for a in self.reduction_attributes],
            'damage_reduction': self.damage_reduction,
        }

    def localize(self):
        return f"" # TODO
        
    @property
    def leader_skill_type(self):
        return 'passive_stats'


# Register the active skill
SkillLoader._register_leader_skill_class(PassiveStatsLS)