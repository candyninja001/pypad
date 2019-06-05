from . import FloorModifier, FloorModifierLoader

class LargeBoardFM(FloorModifier):
    @classmethod
    def handles(self, name):
        return name == '7*6'

    def parse_value(self):
        pass

    def args_to_json(self) -> dict:
        return {}

    def localize(self) -> str:
        return '7x6 board'

    @property
    def floor_modifier_type(self):
        return 'large_board'

    
# register the floor modifier class
FloorModifierLoader._register_floor_modifier_class(LargeBoardFM)