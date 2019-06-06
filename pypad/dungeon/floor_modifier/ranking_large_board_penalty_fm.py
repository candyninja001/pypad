from . import FloorModifier, FloorModifierLoader

class RankingLargeBoardPenaltyFM(FloorModifier):
    @classmethod
    def handles(self, name):
        return name == 'rsd76'

    def parse_value(self):
        self.score_reduction = int(self.value)

    def args_to_json(self) -> dict:
        return {
            'score_reduction': self.score_reduction,
        }

    def localize(self) -> str:
        return '' # TODO

    @property
    def floor_modifier_type(self):
        return 'ranking_large_board_penalty'

    
# register the floor modifier class
FloorModifierLoader._register_floor_modifier_class(RankingLargeBoardPenaltyFM)