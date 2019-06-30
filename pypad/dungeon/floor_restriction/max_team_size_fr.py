from . import FloorRestriction, FloorRestrictionLoader

class MaxTeamSizeFR(FloorRestriction):
    _handle_type = 14

    def parse_args(self):
        self.max_size = self.args[0]

    def args_to_json(self) -> dict:
        return {
            'max_size': self.max_size,
        }

    def localize(self) -> str:
        return f'Teams of {self.max_size} or less'

    @property
    def floor_restriction_type(self):
        return 'max_team_size'


# register the floor restriction class
FloorRestrictionLoader._register_floor_restriction_class(MaxTeamSizeFR)