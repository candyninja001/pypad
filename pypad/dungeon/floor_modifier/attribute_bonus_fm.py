from . import FloorModifier, FloorModifierLoader
from ...attack_attribute import AttackAttribute
from ...common import binary_to_list

class AttributeBonusFM(FloorModifier):
    @classmethod
    def handles(self, name):
        return name == 'battr'

    def parse_value(self):
        args = self.value.split(';')
        self.attributes = tuple(AttackAttribute(a) for a in binary_to_list(int(args[0])))
        self.hp_multiplier = int(args[1]) / 10000
        self.atk_multiplier = int(args[2]) / 10000
        self.rcv_multiplier = int(args[3]) / 10000

    def args_to_json(self) -> dict:
        return {
            'attributes': [a.value for a in self.attributes],
            'hp_multiplier': self.hp_multiplier,
            'atk_multiplier': self.atk_multiplier,
            'rcv_multiplier': self.rcv_multiplier,
        }

    def localize(self) -> str:
        return '' # TODO

    @property
    def floor_modifier_type(self):
        return 'attribute_bonus'

    
# register the floor modifier class
FloorModifierLoader._register_floor_modifier_class(AttributeBonusFM)