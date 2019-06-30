from . import FloorModifier, FloorModifierLoader

class TimeLimitFM(FloorModifier):
    @classmethod
    def handles(self, name):
        return name == 'ta'

    def parse_value(self):
        self.time_limit = int(self.value)

    def args_to_json(self) -> dict:
        return {
            'time_limit': self.time_limit,
        }

    def localize(self) -> str:
        return f'{self.time_limit} second time limit'

    @property
    def floor_modifier_type(self):
        return 'time_limit'

    
# register the floor modifier class
FloorModifierLoader._register_floor_modifier_class(TimeLimitFM)