from . import FloorModifier, FloorModifierLoader

class FixedCardFM(FloorModifier): # TODO rework to contain all cards in one FloorModifier
    @classmethod
    def handles(self, name):
        return name.startswith('fc')

    def parse_value(self):
        self.slot = int(self.name[2:])
        values = [int(x) if x != '' else 0 for x in self.value.split(';')]
        self.card_id = values[0]
        stat_values = values[1:]
        default_stats = [99,0,0,0,99,99] # best guess, [level,+hp,+atk,+rcv,awakenings,skill_level]
        stats = [stat_values[i] if i < len(stat_values) else default_stats[i] for i in range(len(default_stats))]
        self.level = stats[0]
        self.plus_hp = stats[1]
        self.plus_atk = stats[2]
        self.plus_rcv = stats[3]
        self.awakenings = stats[4]
        self.skill_level = stats[5]

    def args_to_json(self) -> dict:
        return {
            'slot': self.slot,
            'card_id': self.card_id,
            'level': self.level,
            'plus_hp': self.plus_hp,
            'plus_atk': self.plus_atk,
            'plus_rcv': self.plus_rcv,
            'awakenings': self.awakenings,
            'skill_level': self.skill_level
        }

    def localize(self) -> str:
        return '' # TODO

    @property
    def floor_modifier_type(self):
        return 'fixed_card'

    
# register the floor modifier class
FloorModifierLoader._register_floor_modifier_class(FixedCardFM)