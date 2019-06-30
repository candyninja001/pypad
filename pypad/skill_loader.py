from .dev import Dev
from .active_skill import ActiveSkill
from .leader_skill import LeaderSkill
from collections import defaultdict
from .common import defaultlist
from .obsolete_skill import ObsoleteSkill

class SkillLoader:
    _registered_active_skill_classes = defaultdict(set)
    _registered_leader_skill_classes = defaultdict(set)

    @classmethod
    def _register_active_skill_class(cls, active_skill_class):
        for internal_skill_type in active_skill_class._handle_types:
            cls._registered_active_skill_classes[internal_skill_type].add(active_skill_class)

    @classmethod
    def _register_leader_skill_class(cls, leader_skill_class):
        for internal_skill_type in leader_skill_class._handle_types:
            cls._registered_leader_skill_classes[internal_skill_type].add(leader_skill_class)

    @classmethod
    def load_active_skill(cls, skill_id, raw_skill, region):
        if len(cls._registered_active_skill_classes[raw_skill[2]]) == 0:
            # no classes are registered
            if len(cls._registered_leader_skill_classes[raw_skill[2]]) == 0:
                Dev.log(f'Unhandled skill [{skill_id}:t_{raw_skill[2]}]')
            return None
        handle_classes = [c for c in cls._registered_active_skill_classes[raw_skill[2]] if c.handles(defaultlist(int, raw_skill))]
        if len(handle_classes) == 1:
            if type(handle_classes[0]) == ObsoleteSkill:
                return None
            return handle_classes[0](skill_id, raw_skill, region)
        if len(handle_classes) > 1:
            Dev.log(f'Active skill [{skill_id}] applies to two or more classes {repr(handle_classes)}, skipping')
            return None
        return None

    @classmethod
    def load_leader_skill(cls, skill_id, raw_skill, region):
        if len(cls._registered_leader_skill_classes[raw_skill[2]]) == 0:
            # no classes are registered
            if len(cls._registered_active_skill_classes[raw_skill[2]]) == 0:
                Dev.log(f'Unhandled skill [{skill_id}:t_{raw_skill[2]}] -> {repr(raw_skill[6:])}')
            return None
        handle_classes = [c for c in cls._registered_leader_skill_classes[raw_skill[2]] if c.handles(defaultlist(int, raw_skill))]
        if len(handle_classes) == 1:
            if type(handle_classes[0]) == ObsoleteSkill:
                return None
            return handle_classes[0](skill_id, raw_skill, region)
        if len(handle_classes) > 1:
            Dev.log(f'Leader skill [{skill_id}] applies to two or more classes {repr(handle_classes)}, skipping')
            return None
        return None


# Register the obsolete skill
SkillLoader._register_active_skill_class(ObsoleteSkill)
SkillLoader._register_leader_skill_class(ObsoleteSkill)

# Import all active skill classes for loading

from .active_skill.attack_as import AttackAS
from .active_skill.attribute_atk_and_rcv_boost_as import AttributeATKAndRCVBoostAS
from .active_skill.attribute_shield_as import AttributeShieldAS
from .active_skill.awakening_atk_boost_as import AwakeningATKBoostAS
from .active_skill.awakening_heal_as import AwakeningHealAS
from .active_skill.awakening_shield_as import AwakeningShieldAS
from .active_skill.board_change_as import BoardChangeAS
from .active_skill.board_change_with_path_as import BoardChangeWithPathAS
from .active_skill.board_refresh_as import BoardRefreshAS
from .active_skill.card_attribute_change_as import CardAttributeChangeAS
from .active_skill.change_skyfall_as import ChangeSkyfallAS
from .active_skill.column_change_as import ColumnChangeAS
from .active_skill.counter_attack_as import CounterAttackAS
from .active_skill.create_orb_pattern_as import CreateOrbPatternAS
from .active_skill.damage_shield_as import DamageShieldAS
from .active_skill.defense_reduction_as import DefenseReductionAS
from .active_skill.delay_as import DelayAS
from .active_skill.double_orb_change import DoubleOrbChangeAS
from .active_skill.enemy_attribute_change_as import EnemyAttributeChangeAS
from .active_skill.enhance_orbs_as import EnhanceOrbsAS
from .active_skill.enhance_skyfall_as import EnhanceSkyfallAS
from .active_skill.extra_combo_as import ExtraComboAS
from .active_skill.gravity_max_as import GravityMaxAS
from .active_skill.gravity_normal_as import GravityNormalAS
from .active_skill.laser_as import LaserAS
from .active_skill.leader_swap_as import LeaderSwapAS
from .active_skill.lock_orbs_as import LockOrbsAS
from .active_skill.mass_attack_as import MassAttackAS
from .active_skill.move_orbs_freely_as import MoveOrbsFreelyAS
from .active_skill.move_time_flat_as import MoveTimeFlatAS
from .active_skill.move_time_percentage_as import MoveTimePercentageAS
from .active_skill.multihit_laser_as import MultihitLaserAS
from .active_skill.no_skyfall_as import NoSkyfallAS
from .active_skill.pierce_damage_void_as import PierceDamageVoidAS
from .active_skill.poison_as import PoisonAS
from .active_skill.random_orb_change_as import RandomOrbChangeAS
from .active_skill.recover_as import RecoverAS
from .active_skill.reduce_unmatchable_debuff_as import ReduceUnmatchableDebuffAS
from .active_skill.row_change_as import RowChangeAS
from .active_skill.single_orb_change_as import SingleOrbChangeAS
from .active_skill.skill_charge_as import SkillChargeAS
from .active_skill.spawn_orbs_as import SpawnOrbsAS
from .active_skill.suicide_as import SuicideAS
from .active_skill.type_atk_boost_as import TypeATKBoostAS
from .active_skill.unlock_orbs_as import UnlockOrbsAS
from .active_skill.void_absorb_as import VoidAbsorbAS

def _register_special_active_skill_classes():
    from .active_skill.combine_active_skills_as import CombineActiveSkillsAS
    from .active_skill.random_active_skill_as import RandomActiveSkillAS


# Import all leader skill classes for loading

from .leader_skill.attribute_match_ls import AttributeMatchLS
from .leader_skill.auto_recover_ls import AutoRecoverLS
from .leader_skill.bonus_attack_ls import BonusAttackLS
from .leader_skill.bonus_move_time_ls import BonusMoveTimeLS
from .leader_skill.coin_drop_rate_ls import CoinDropRateLS
from .leader_skill.collab_stats_ls import CollabStatsLS
from .leader_skill.color_cross_ls import ColorCross
from .leader_skill.combo_match_exact_ls import ComboMatchExactLS
from .leader_skill.combo_match_ls import ComboMatchLS
from .leader_skill.connected_match_ls import ConnectedMatchLS
from .leader_skill.counter_attack import CounterAttackLS
from .leader_skill.drumming_sound_ls import DrummingSoundLS
from .leader_skill.egg_drop_rate_ls import EggDropRateLS
from .leader_skill.five_orb_one_enhance_ls import FiveOrbOneEnhanceLS
from .leader_skill.fixed_move_time_ls import FixedMoveTimeLS
from .leader_skill.heal_tpa_ls import HealTPALS
from .leader_skill.heart_cross_ls import HeartCrossLS
from .leader_skill.l_match_ls import LMatchLS
from .leader_skill.large_board_ls import LargeBoardLS
from .leader_skill.minimum_match_size_ls import MinimumMatchSizeLS
from .leader_skill.multi_attribute_match_ls import MultiAttributeMatchLS
from .leader_skill.multi_connected_match_ls import MultiConnectedMatchLS
from .leader_skill.multiplayer_stats_ls import MultiplayerStatsLS
from .leader_skill.no_skyfall_ls import NoSkyfallLS
from .leader_skill.orbs_remaining_ls import OrbsRemainingLS
from .leader_skill.passive_stats_dual_ls import PassiveStatsDualLS
from .leader_skill.passive_stats_ls import PassiveStatsLS
from .leader_skill.rank_experience_rate_ls import RankExperienceRateLS
from .leader_skill.resolve_ls import ResolveLS
from .leader_skill.skill_used_ls import SkillUsedLS
from .leader_skill.team_build_ls import TeamBuildLS
from .leader_skill.threshold_stats_above_ls import ThresholdStatsAboveLS
from .leader_skill.threshold_stats_below_ls import ThresholdStatsBelowLS
from .leader_skill.threshold_stats_dual_ls import ThresholdStatsDualLS

def _register_special_leader_skill_classes():
    from .leader_skill.combine_leader_skills_ls import CombineLeaderSkillsAS