from . import FloorRestriction, FloorRestrictionLoader

class MaxTeamCostFR(FloorRestriction):
    _handle_type = 2

    def parse_args(self):
        self.max_cost = self.args[0]

    def args_to_json(self) -> dict:
        return {
            'max_cost': self.max_cost,
        }

    def localize(self) -> str:
        return f'Max team cost of {self.max_cost}'

    @property
    def floor_restriction_type(self):
        return 'max_team_cost'


# register the floor restriction class
FloorRestrictionLoader._register_floor_restriction_class(MaxTeamCostFR)