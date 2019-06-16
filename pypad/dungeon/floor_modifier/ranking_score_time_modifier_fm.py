from . import FloorModifier, FloorModifierLoader

class RankingScoreTimeModifierFM(FloorModifier):
    @classmethod
    def handles(self, name):
        return name == 'rsmtm'

    def parse_value(self):
        self.time_score_modifier = int(self.value) / 100

    def args_to_json(self) -> dict:
        return {
            'time_score_modifier': self.time_score_modifier,
        }

    def localize(self) -> str:
        return '{self.time_score_modifier}x score from remaining time'

    @property
    def floor_modifier_type(self):
        return 'ranking_score_time_modifier'

    
# register the floor modifier class
FloorModifierLoader._register_floor_modifier_class(RankingScoreTimeModifierFM)