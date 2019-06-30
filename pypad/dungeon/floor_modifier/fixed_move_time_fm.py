from . import FloorModifier, FloorModifierLoader

class FixedMoveTimeFM(FloorModifier):
    @classmethod
    def handles(self, name):
        return name == 'ft'

    def parse_value(self):
        self.fixed_time = int(self.value) / 10

    def args_to_json(self) -> dict:
        return {
            'fixed_time': self.fixed_time
        }

    def localize(self) -> str:
        return f'{self.fixed_time} seconds fixed move time'

    @property
    def floor_modifier_type(self):
        return 'fixed_move_time'

    
# register the floor modifier class
FloorModifierLoader._register_floor_modifier_class(FixedMoveTimeFM)