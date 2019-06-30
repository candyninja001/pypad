from . import FloorModifier, FloorModifierLoader
import re
from ...awakening import Awakening

class RankingScoreAwakeningModifierFM(FloorModifier):
    @classmethod
    def handles(self, name):
        return re.match(r'rsm\d+', name)

    def parse_value(self):
        self.awakening = Awakening(int(self.name[3:]))
        self.score_modifier = int(self.value) / 100

    def args_to_json(self) -> dict:
        return {
            'awakening': self.awakening.value,
            'score_modifier': self.score_modifier,
        }

    def localize(self) -> str:
        return '' # TODO

    @property
    def floor_modifier_type(self):
        return 'ranking_score_awakening_modifier'

    
# register the floor modifier class
FloorModifierLoader._register_floor_modifier_class(RankingScoreAwakeningModifierFM)