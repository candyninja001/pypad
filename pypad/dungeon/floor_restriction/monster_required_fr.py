from . import FloorRestriction, FloorRestrictionLoader

class MonsterRequiredFR(FloorRestriction):
    _handle_type = 13

    def parse_args(self):
        self.monster_id = self.args[0]

    def args_to_json(self) -> dict:
        return {
            'monster_id': self.monster_id
        }

    def localize(self) -> str:
        return f'' # TODO

    @property
    def floor_restriction_type(self):
        return 'monster_required'


# register the floor restriction class
FloorRestrictionLoader._register_floor_restriction_class(MonsterRequiredFR)