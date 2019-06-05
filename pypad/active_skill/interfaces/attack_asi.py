import abc
from enum import Enum
from ...attack_attribute import AttackAttribute

class AttackDamageCalculationType(Enum):
    UNKNOWN = -1
    FIXED_DAMAGE = 0
    X_ATK = 1
    X_TEAM_ATK = 2
    X_TEAM_HP = 3
    GRUDGE_X_ATK = 4
    RANDOM_X_ATK = 5


# Interface for active skills that launch an attack (not lasers)
class AttackASI(abc.ABC):
    def is_attack(self) -> bool:
        return True

    # Does the skill hit multiple or one target
    @abc.abstractmethod
    def is_attack_mass_attack(self) -> bool:
        pass

    # What calculation is used for the attack damage
    @abc.abstractmethod
    def get_attack_damage_calculation_type(self) -> AttackDamageCalculationType:
        pass

    # What is the fixed damage value, only for FIXED_DAMAGE
    def get_attack_fixed_damage(self) -> int:
        return 0

    # What is the multiplier
    def get_attack_multipliers(self) -> (float,float):
        return (0.0,0.0)

    # What team attributes are used for X_TEAM_ATK
    def get_attack_team_attributes(self) -> tuple(AttackAttribute):
        return tuple()

    # What attribute is the attack, NONE if uses card attribute
    @abc.abstractmethod
    def get_attack_fixed_attack_attribute(self) -> AttackAttribute:
        pass

    # Does the attack recover player HP
    def is_attack_drain(self) -> bool:
        return False

    # What multiple of damage is healed as player HP
    def get_attack_drain_multiplier(self) -> float:
        return 0.0

    # What attribute enemy can be targeted with this attack, NONE if all
    def get_attack_target_attributes(self) -> AttackAttribute:
        return AttackAttribute.NONE

    # Does the attack reduce player HP
    def is_attack_suicide(self) -> bool:
        return False

    # What percentage of player HP remains after attacking
    def get_attack_suicide_percentage(self) -> float:
        return 1.0