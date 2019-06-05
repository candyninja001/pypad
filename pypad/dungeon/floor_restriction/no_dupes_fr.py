from . import FloorRestriction, FloorRestrictionLoader

class NoDupesFR(FloorRestriction):
    _handle_type = 10

    def parse_args(self):
        pass

    def args_to_json(self) -> dict:
        return {}

    def localize(self) -> str:
        return f'No dupes' # TODO

    @property
    def floor_restriction_type(self):
        return 'no_dupes'


# register the floor restriction class
FloorRestrictionLoader._register_floor_restriction_class(NoDupesFR)