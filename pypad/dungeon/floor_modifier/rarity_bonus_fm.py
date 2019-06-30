from . import FloorModifier, FloorModifierLoader
from ...common import binary_to_list

class RarityBonusFM(FloorModifier):
    @classmethod
    def handles(self, name):
        return name == 'brare'

    def parse_value(self):
        args = self.value.split(';')
        self.rarities = tuple(r for r in binary_to_list(int(args[0])))
        self.hp_multiplier = int(args[1]) / 10000
        self.atk_multiplier = int(args[2]) / 10000
        self.rcv_multiplier = int(args[3]) / 10000

    def args_to_json(self) -> dict:
        return {
            'rarities': [r for r in self.rarities],
            'hp_multiplier': self.hp_multiplier,
            'atk_multiplier': self.atk_multiplier,
            'rcv_multiplier': self.rcv_multiplier,
        }

    def localize(self) -> str:
        return '' # TODO

    @property
    def floor_modifier_type(self):
        return 'rarity_bonus'

    
# register the floor modifier class
FloorModifierLoader._register_floor_modifier_class(RarityBonusFM)