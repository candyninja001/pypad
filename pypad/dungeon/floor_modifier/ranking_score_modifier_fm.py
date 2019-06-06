from . import FloorModifier, FloorModifierLoader
from ...awakening import Awakening

class RankingScoreModifierFM(FloorModifier):
    @classmethod
    def handles(self, name):
        return name.startswith('rsm') and name != 'rsma'

    def parse_value(self):
        self.awakening = Awakening(int(self.name[3:]))
        self.score_multiplier = int(self.value) / 100

    def args_to_json(self) -> dict:
        return {
            'awakening': self.awakening.value,
            'score_multiplier': self.score_multiplier,
        }

    def localize(self) -> str:
        return '' # TODO

    @property
    def floor_modifier_type(self):
        return 'ranking_score_modifier'

    
# register the floor modifier class
FloorModifierLoader._register_floor_modifier_class(RankingScoreModifierFM)