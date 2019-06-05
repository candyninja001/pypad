from . import FloorModifier, FloorModifierLoader

class EnemyHPMultiplierFM(FloorModifier):
    @classmethod
    def handles(self, name):
        return name == 'hp'

    def parse_value(self):
        self.hp_multiplier = int(self.value) / 10000

    def args_to_json(self) -> dict:
        return {
            'hp_multiplier': self.hp_multiplier,
        }

    def localize(self) -> str:
        return '' # TODO

    @property
    def floor_modifier_type(self):
        return 'enemy_hp_multiplier'

    
# register the floor modifier class
FloorModifierLoader._register_floor_modifier_class(EnemyHPMultiplierFM)