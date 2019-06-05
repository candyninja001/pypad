from . import FloorModifier, FloorModifierLoader

class NoSkyfallFM(FloorModifier):
    @classmethod
    def handles(self, name):
        return name == 'ndf'

    def parse_value(self):
        pass

    def args_to_json(self) -> dict:
        return {}

    def localize(self) -> str:
        return 'No skyfall orbs'

    @property
    def floor_modifier_type(self):
        return 'no_skyfall'

    
# register the floor modifier class
FloorModifierLoader._register_floor_modifier_class(NoSkyfallFM)