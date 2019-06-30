from . import FloorRestriction, FloorRestrictionLoader

class RoguelikeFR(FloorRestriction):
    _handle_type = 11

    def parse_args(self):
        pass # TODO

    def args_to_json(self) -> dict:
        return {f'arg_'+i:self.args[i] for i in range(len(self.args))}

    def localize(self) -> str:
        return f'' # TODO

    @property
    def floor_restriction_type(self):
        return 'roguelike'


# register the floor restriction class
FloorRestrictionLoader._register_floor_restriction_class(RoguelikeFR)