from . import FloorModifier, FloorModifierLoader

class EnemyDefenseMultiplierFM(FloorModifier):
    @classmethod
    def handles(self, name):
        return name == 'df'

    def parse_value(self):
        self.defense_multiplier = int(self.value) / 10000

    def args_to_json(self) -> dict:
        return {
            'defense_multiplier': self.defense_multiplier,
        }

    def localize(self) -> str:
        return '' # TODO

    @property
    def floor_modifier_type(self):
        return 'enemy_defense_multiplier'

    
# register the floor modifier class
FloorModifierLoader._register_floor_modifier_class(EnemyDefenseMultiplierFM)