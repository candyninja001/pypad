from . import FloorModifier, FloorModifierLoader

class EnvironmentFM(FloorModifier):
    @classmethod
    def handles(self, name):
        return name == 'dg'

    def parse_value(self):
        self.environment = int(self.value)  # TODO create FloorEnvironment enum

    def args_to_json(self) -> dict:
        return {
            'environment': self.environment,
        }

    def localize(self) -> str:
        return '' # TODO

    @property
    def floor_modifier_type(self):
        return 'environment'

    
# register the floor modifier class
FloorModifierLoader._register_floor_modifier_class(EnvironmentFM)