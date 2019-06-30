from . import FloorModifier, FloorModifierLoader

class ObsoleteFM(FloorModifier):
    @classmethod
    def handles(self, name):
        return name == 'rsma'

    def parse_value(self):
        pass

    def args_to_json(self) -> dict:
        return {
            'name': self.name,
        }

    def localize(self) -> str:
        return ''

    @property
    def floor_modifier_type(self):
        return 'obsolete'

    
# register the floor modifier class
FloorModifierLoader._register_floor_modifier_class(ObsoleteFM)