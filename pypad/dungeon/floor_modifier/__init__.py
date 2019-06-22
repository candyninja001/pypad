from collections import defaultdict
from ...dev import Dev

class FloorModifier:
    @classmethod
    def handles(cls, name):
        return False

    def __init__(self, name, value):
        self.name = name
        self.value = value
        self.parse_value()

    def parse_value(self):
        pass

    def to_json(self, localize=False) -> dict:
        skill_json = {
            'name': self.name,
            'args': self.args_to_json(),
        }
        if localize:
            skill_json['localization'] = self.localize()
        return skill_json

    def args_to_json(self) -> dict:
        return {'value': self.value}

    def localize(self) -> str:
        return ''

    @property
    def floor_modifier_type(self):
        return 'default_floor_modifier_type'
    
class FloorModifierLoader:
    _registered_floor_modifier_classes = set()

    @classmethod
    def _register_floor_modifier_class(cls, floor_modifier_class):
        cls._registered_floor_modifier_classes.add(floor_modifier_class)

    @classmethod
    def load_floor_modifier(cls, name, value):
        if name == '' and value == '':
            return None
        handle_classes = [c for c in cls._registered_floor_modifier_classes if c.handles(name)]
        if len(handle_classes) == 1:
            fm = handle_classes[0](name, value)
            if type(fm) == ObsoleteFM:
                return None
            return fm
        if len(handle_classes) > 1:
            Dev.log(f'Floor modifier "{name}":"{value}" applies to two or more classes, skipping')
            return None
        Dev.log(f'Floor modifier "{name}":"{value}" not handled, skipping')
        return None

from .obsolete_fm import ObsoleteFM

from .attribute_bonus_fm import AttributeBonusFM
from .enemy_attack_multiplier_fm import EnemyAttackMultiplierFM
from .enemy_defense_multiplier_fm import EnemyDefenseMultiplierFM
from .enemy_hp_multiplier_fm import EnemyHPMultiplierFM
from .environment_fm import EnvironmentFM
from .fever_mode_fm import FeverModeFM
from .fixed_hp_fm import FixedHPFM
from .fixed_move_time_fm import FixedMoveTimeFM
from .large_board_fm import LargeBoardFM
from .no_skyfall_fm import NoSkyfallFM
from .ranking_large_board_penalty_fm import RankingLargeBoardPenaltyFM
from .ranking_score_time_modifier_fm import RankingScoreTimeModifierFM
from .rarity_bonus_fm import RarityBonusFM
from .small_board_fm import SmallBoardFM
from .time_limit_fm import TimeLimitFM
from .type_bonus_fm import TypeBonusFM

# TODO rework these to be collect modifiers of all names, not just one at a time
from .d_message_fm import DMessageFM
from .fixed_card_fm import FixedCardFM
from .s_message_fm import SMessageFM
from .ranking_score_awakening_modifier_fm import RankingScoreAwakeningModifierFM
