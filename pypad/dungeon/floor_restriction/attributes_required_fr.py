from . import FloorRestriction, FloorRestrictionLoader
from ...attack_attribute import AttackAttribute

class AttributesRequiredFR(FloorRestriction):
    _handle_type = 9

    def parse_args(self):
        self.attributes = tuple(AttackAttribute(a-1) for a in self.args)

    def args_to_json(self) -> dict:
        return {
            'attributes': [a.value for a in self.attributes],
        }

    def localize(self) -> str:
        return f'' # TODO

    @property
    def floor_restriction_type(self):
        return 'attributes_required'


# register the floor restriction class
FloorRestrictionLoader._register_floor_restriction_class(AttributesRequiredFR)