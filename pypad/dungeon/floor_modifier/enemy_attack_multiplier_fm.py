from . import FloorModifier, FloorModifierLoader

class EnemyAttackMultiplierFM(FloorModifier):
    @classmethod
    def handles(self, name):
        return name == 'at'

    def parse_value(self):
        self.attack_multiplier = int(self.value) / 10000

    def args_to_json(self) -> dict:
        return {
            'attack_multiplier': self.attack_multiplier,
        }

    def localize(self) -> str:
        return '' # TODO

    @property
    def floor_modifier_type(self):
        return 'enemy_attack_multiplier'

    
# register the floor modifier class
FloorModifierLoader._register_floor_modifier_class(EnemyAttackMultiplierFM)