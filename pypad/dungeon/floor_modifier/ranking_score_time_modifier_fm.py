from . import FloorModifier, FloorModifierLoader

class RankingScoreTimeModifierFM(FloorModifier):
    @classmethod
    def handles(self, name):
        return name == 'rsmtm'

    def parse_value(self):
        self.score_modifier = int(self.value) / 100

    def args_to_json(self) -> dict:
        return {
            'score_modifier': self.score_modifier,
        }

    def localize(self) -> str:
        return f'{self.score_modifier}x score from remaining time'

    @property
    def floor_modifier_type(self):
        return 'ranking_score_time_modifier'

    
# register the floor modifier class
FloorModifierLoader._register_floor_modifier_class(RankingScoreTimeModifierFM)