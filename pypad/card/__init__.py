from ..region import Region
from ..attack_attribute import AttackAttribute
from ..monster_type import MonsterType
from ..awakening import Awakening
from ..latent_awakening import LatentAwakening
from ..read_only_property import read_only_property

class Card:
    _loaded = False

    def __init__(self, raw_card, region=Region.NA):
        self.region = region

        self.id = raw_card[0]
        self.name = raw_card[1]
        self.attribute = AttackAttribute(raw_card[2])
        self.subattribute = AttackAttribute(raw_card[3])
        # 4 is_ultimate in Evolution
        self.types = [MonsterType(raw_card[5])]
        self.types.append(MonsterType(raw_card[6]))
        self.rarity = raw_card[7]
        self.cost = raw_card[8]
        self.size = raw_card[9]
        self.max_level = raw_card[10]
        self.feed_experience_per_level = raw_card[11] / 4
        self.released = raw_card[12] == 100
        self.sell_value_coin_per_level = raw_card[13] / 10
        self.hp_minimum = raw_card[14]
        self.hp_maximum = raw_card[15]
        self.hp_curve = raw_card[16]
        self.atk_minimum = raw_card[17]
        self.atk_maximum = raw_card[18]
        self.atk_curve = raw_card[19]
        self.rcv_minimum = raw_card[20]
        self.rcv_maximum = raw_card[21]
        self.rcv_curve = raw_card[22]
        self.max_experience = raw_card[23]
        self.experience_curve = raw_card[24]
        self.active_skill_id = raw_card[25]
        self.leader_skill_id = raw_card[26]

        # 27 - 39 stats in Enemy

        # 40 - 50 Evolution

        # 51 - 57 skills in Enemy

        enemy_skill_count = raw_card[57]
        i = 3 * enemy_skill_count

        awakening_count = raw_card[i+58]
        self.awakenings = tuple(Awakening(raw_card[i+59+a]) for a in range(awakening_count))
        j = i + awakening_count
        
        self.super_awakenings = tuple(Awakening(int(a)) for a in raw_card[j+59].split(',') if a != '')
        self.base_evo_id = raw_card[j+60]
        self.group = raw_card[j+61] # TODO create a Group class or enum
        self.types.append(MonsterType(raw_card[j+62]))
        self.types = tuple(t for t in self.types if t != MonsterType.NONE)
        self.sell_value_mp = raw_card[j+63]
        self.latent_on_fuse = LatentAwakening(raw_card[j+64])
        self.collab = raw_card[j+65] # TODO create a Collab class or enum
        self.inheritable = raw_card[j+66] = 3
        self.furigana = raw_card[j+67]
        self.limitbreak_stat_increase = raw_card[j+68] / 100
        self.voice = raw_card[j+69] # TODO create a Voice class or enum
        self.orb_skin = raw_card[j+70] # TODO create an OrbSkin class or enum

        self._loaded = True


    def _get_curve_value(self, min_stat, max_stat, curve, max_level, level):
        return round(min_stat + (max_stat - min_stat) * ((level - 1) / (max_level - 1)) ** curve)

    def _get_stat_at_level(self, min_stat, max_stat, curve, level):
        if type(level) != int:
            raise ValueError('level must be an int')
        if level < 1:
            raise ValueError('level must be greater than or equal to 1')
        if level <= self.max_level:
            return self._get_curve_value(min_stat, max_stat, curve, self.max_level, level)
        if self.max_level == 99 and self.limitbreakable:
            if level <= 110:
                return max_stat * (1 + self.limitbreak_stat_increase * ((level - 99) / 11))
            raise ValueError('level must be less than or equal to 110')
        raise ValueError('level must be less than or equal to 99')

    def get_hp_at_level(self, level):
        return self._get_stat_at_level(self.hp_minimum, self.hp_maximum, self.hp_curve, level)

    def get_atk_at_level(self, level):
        return self._get_stat_at_level(self.atk_minimum, self.atk_maximum, self.atk_curve, level)

    def get_rcv_at_level(self, level):
        return self._get_stat_at_level(self.rcv_minimum, self.rcv_maximum, self.rcv_curve, level)

    def to_json(self) -> dict:
        return {
            'id': self.id,
            'name': self.name,
            'attribute': self.attribute.value,
            'subattribute': self.subattribute.value,
            'types': [t.value for t in self.types],
            'rarity': self.rarity,
            'cost': self.cost,
            'max_level': self.max_level,
            'feed_experience_per_level': self.feed_experience_per_level,
            'released': self.released,
            'sell_value_coin_per_level': self.sell_value_coin_per_level,
            'hp_minimum': self.hp_minimum,
            'hp_maximum': self.hp_maximum,
            'hp_curve': self.hp_curve,
            'atk_minimum': self.atk_minimum,
            'atk_maximum': self.atk_maximum,
            'atk_curve': self.atk_curve,
            'rcv_minimum': self.rcv_minimum,
            'rcv_maximum': self.rcv_maximum,
            'rcv_curve': self.rcv_curve,
            'max_experience': self.max_experience,
            'experience_curve': self.experience_curve,
            'active_skill_id': self.active_skill_id,
            'leader_skill_id': self.leader_skill_id,
            'awakenings': [a.value for a in self.awakenings],
            'super_awakenings': [a.value for a in self.super_awakenings],
            'base_evo_id': self.base_evo_id,
            'group': self.group,
            'sell_value_mp': self.sell_value_mp,
            'latent_on_fuse': self.latent_on_fuse.value,
            'collab': self.collab,
            'inheritable': self.inheritable,
            'furigana': self.furigana,
            'limitbreakable': self.limitbreakable,
            'limitbreak_stat_increase': self.limitbreak_stat_increase,
        }
        
    @read_only_property
    def limitbreakable(self):
        return self.limitbreak_stat_increase > 0.0

    # protect the read only attributes
    def __setattr__(self, name, value):
        if (self._loaded):
            raise Exception('Cannot set attributes of Card')
        self.__dict__[name] = value
            