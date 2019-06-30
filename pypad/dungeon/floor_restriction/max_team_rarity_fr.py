from . import FloorRestriction, FloorRestrictionLoader

class MaxTeamRarityFR(FloorRestriction):
    _handle_type = 4

    def parse_args(self):
        self.max_rarity = self.args[0]

    def args_to_json(self) -> dict:
        return {
            'max_rarity': self.max_rarity,
        }

    def localize(self) -> str:
        return f'Max team rarity of {self.max_rarity}'

    @property
    def floor_restriction_type(self):
        return 'max_team_rarity'


# register the floor restriction class
FloorRestrictionLoader._register_floor_restriction_class(MaxTeamRarityFR)