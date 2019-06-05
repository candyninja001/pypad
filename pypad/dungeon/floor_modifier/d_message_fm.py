from . import FloorModifier, FloorModifierLoader

class DMessageFM(FloorModifier):
    @classmethod
    def handles(self, name):
        return name.startswith('dmsg')

    def parse_value(self):
        self.message_number = int(self.name[4:])
        self.message = self.value

    def args_to_json(self) -> dict:
        return {
            'message_number': self.message_number,
            'message': self.message,
        }

    def localize(self) -> str:
        return '' # TODO

    @property
    def floor_modifier_type(self):
        return 'd_message'

    
# register the floor modifier class
FloorModifierLoader._register_floor_modifier_class(DMessageFM)