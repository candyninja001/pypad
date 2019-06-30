from . import FloorRestriction, FloorRestrictionLoader
from ...monster_type import MonsterType

class TypeRestrictionFR(FloorRestriction):
    _handle_type = 7

    def parse_args(self):
        self.type = MonsterType(self.args[0])

    def args_to_json(self) -> dict:
        return {
            'type': self.type.value,
        }

    def localize(self) -> str:
        return f'' # TODO

    @property
    def floor_restriction_type(self):
        return 'type_restriction'


# register the floor restriction class
FloorRestrictionLoader._register_floor_restriction_class(TypeRestrictionFR)