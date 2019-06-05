from . import FloorModifier, FloorModifierLoader

class FixedHPFM(FloorModifier):
    @classmethod
    def handles(self, name):
        return name == 'hpfix'

    def parse_value(self):
        self.hp = int(self.value)

    def args_to_json(self) -> dict:
        return {
            'hp': self.hp,
        }

    def localize(self) -> str:
        return f'Fixed {self.hp} team HP'

    @property
    def floor_modifier_type(self):
        return 'fixed_hp'

    
# register the floor modifier class
FloorModifierLoader._register_floor_modifier_class(FixedHPFM)