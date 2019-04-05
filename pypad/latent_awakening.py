from enum import Enum
from .monster_type import MonsterType

class LatentAwakening(Enum):
    NONE = (0, 1, [])
    IMPROVED_HP = (1, 1, [])
    IMPROVED_ATK = (2, 1, [])
    IMPROVED_RCV = (3, 1, [])
    EXTENDED_MOVE_TIME = (4, 1, [])
    AUTO_HEAL = (5, 1, [])
    FIRE_DAMAGE_REDUCTION = (6, 1, [])
    WATER_DAMAGE_REDUCTION = (7, 1, [])
    WOOD_DAMAGE_REDUCTION = (8, 1, [])
    LIGHT_DAMAGE_REDUCTION = (9, 1, [])
    DARK_DAMAGE_REDUCTION = (10, 1, [])
    SKILL_DELAY_RESISTANCE = (11, 1, [])
    ALL_STATS_ENHANCED = (12, 2, [])
    EVO_MATERIAL_KILLER = (16, 2, [])
    AWOKEN_MATERIAL_KILLER = (17, 2, [])
    ENHANCED_MATERIAL_KILLER = (18, 2, [])
    REDEEMABLE_MATERIAL_KILLER = (19, 2, [])
    GOD_KILLER = (20, 2, [MonsterType.BALANCED, MonsterType.DEVIL, MonsterType.MACHINE])
    DRAGON_KILLER = (21, 2, [MonsterType.BALANCED, MonsterType.HEALER])
    DEVIL_KILLER = (22, 2, [MonsterType.BALANCED, MonsterType.GOD, MonsterType.ATTACKER])
    MACHINE_KILLER = (23, 2, [MonsterType.BALANCED, MonsterType.DRAGON, MonsterType.PHYSICAL])
    BALANCED_KILLER = (24, 2, [MonsterType.BALANCED, MonsterType.MACHINE])
    ATTACKER_KILLER = (25, 2, [MonsterType.BALANCED, MonsterType.HEALER])
    PHYSICAL_KILLER = (26, 2, [MonsterType.BALANCED, MonsterType.ATTACKER])
    HEALER_KILLER = (27, 2, [MonsterType.BALANCED, MonsterType.DRAGON, MonsterType.PHYSICAL])
    IMPROVED_HP_PLUS = (28, 2, [])
    IMPROVED_ATK_PLUS = (29, 2, [])
    IMPROVED_RCV_PLUS = (30, 2, [])
    EXTENDED_MOVE_TIME_PLUS = (31, 2, [])
    FIRE_DAMAGE_REDUCTION_PLUS = (32, 2, [])
    WATER_DAMAGE_REDUCTION_PLUS = (33, 2, [])
    WOOD_DAMAGE_REDUCTION_PLUS = (34, 2, [])
    LIGHT_DAMAGE_REDUCTION_PLUS = (35, 2, [])
    DARK_DAMAGE_REDUCTION_PLUS = (36, 2, [])

    def __new__(cls, value, slots=None, types=None):
        if slots == None and types == None: # value lookup instead of creation
            return Enum.__new__(cls, value)
            
        latent = object.__new__(cls)
        latent._value_ = value
        latent._slots = slots
        latent._types = types
        return latent

    def slots(self) -> int:
        return self._slots

    def allowed_types(self) -> [MonsterType]:
        if len(self._types) == 0:
            return [t for t in MonsterType if t != MonsterType.NONE]
        return self._types

    def allowed_for_types(self, types: (MonsterType,)) -> bool:
        if len(self._types) == 0:
            return True
        return any(t in self._types for t in types)

    @classmethod
    def get_killers_for_types(cls, types: (MonsterType,)) -> ['LatentAwakening']:
        return [l for l in LatentAwakening if any(t in l._types for t in types)]

    @classmethod
    def get_latents_for_types(cls, types: (MonsterType,)) -> ['LatentAwakening']:
        return [l for l in LatentAwakening if l.allowed_for_types(types)]
    