from . import FloorModifier, FloorModifierLoader

class SmallBoardFM(FloorModifier):
    @classmethod
    def handles(self, name):
        return name == '5*4'

    def parse_value(self):
        pass

    def args_to_json(self) -> dict:
        return {}

    def localize(self) -> str:
        return '5x4 board'

    @property
    def floor_modifier_type(self):
        return 'small_board'

    
# register the floor modifier class
FloorModifierLoader._register_floor_modifier_class(SmallBoardFM)