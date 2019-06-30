from . import FloorModifier, FloorModifierLoader

class FeverModeFM(FloorModifier):
    @classmethod
    def handles(self, name):
        return name == 'tvm'

    def parse_value(self):
        pass

    def args_to_json(self) -> dict:
        return {}

    def localize(self) -> str:
        return 'Fever Mode'

    @property
    def floor_modifier_type(self):
        return 'fever_mode'

    
# register the floor modifier class
FloorModifierLoader._register_floor_modifier_class(FeverModeFM)