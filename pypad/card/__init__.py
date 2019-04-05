from ..region import Region
from ..attack_attribute import AttackAttribute
from ..monster_type import MonsterType
from ..awakening import Awakening
from ..latent_awakening import LatentAwakening
from ..read_only_property import read_only_property

class Card:
    def __init__(self, raw_card, region=Region.NA):
        self._region = region

        self._id = raw_card[0]
        self._name = raw_card[1]
        self._attribute = AttackAttribute(raw_card[2])
        self._subattribute = AttackAttribute(raw_card[3])
        # 4 is_ultimate in Evolution
        self._types = [MonsterType(raw_card[5])]
        self._types.append(MonsterType(raw_card[6]))
        self._rarity = raw_card[7]
        self._cost = raw_card[8]
        self._size = raw_card[9]
        self._max_level = raw_card[10]
        self._feed_experience_per_level = raw_card[11] / 4
        self._released = raw_card[12] == 100
        self._sell_value_coin_per_level = raw_card[13] / 10
        self._hp_minimum = raw_card[14]
        self._hp_maximum = raw_card[15]
        self._hp_curve = raw_card[16]
        self._atk_minimum = raw_card[17]
        self._atk_maximum = raw_card[18]
        self._atk_curve = raw_card[19]
        self._rcv_minimum = raw_card[20]
        self._rcv_maximum = raw_card[21]
        self._rcv_curve = raw_card[22]
        self._max_experience = raw_card[23]
        self._experience_curve = raw_card[24]
        self._active_skill_id = raw_card[25]
        self._leader_skill_id = raw_card[26]

        # 27 - 39 stats in Enemy

        # 40 - 50 Evolution

        # 51 - 57 skills in Enemy

        enemy_skill_count = raw_card[57]
        i = 3 * enemy_skill_count

        awakening_count = raw_card[i+58]
        self._awakenings = tuple(Awakening(raw_card[i+59+a]) for a in range(awakening_count))
        
        j = i + awakening_count
        self._super_awakenings = tuple(Awakening(int(a)) for a in raw_card[j+59].split(',') if a != '')
        self._base_evo_id = raw_card[j+60]
        self._group = raw_card[j+61] # TODO create a Group class or enum
        self._types.append(MonsterType(raw_card[j+62]))
        self._types = tuple(t for t in self._types if t != MonsterType.NONE)
        self._sell_value_mp = raw_card[j+63]
        self._latent_on_fuse = LatentAwakening(raw_card[j+64])
        self._collab = raw_card[j+65] # TODO create a Collab class or enum
        self._inheritable = raw_card[j+66] = 3
        self._furigana = raw_card[j+67]
        self._limitbreak_stat_increase = raw_card[j+68] / 100
        self._voice = raw_card[j+69] # TODO create a Voice class or enum
        self._orb_skin = raw_card[j+70] # TODO create an OrbSkin class or enum

        # add the read only properties
        property_names = [n for n in vars(self).keys() if n[0] == '_' and n[1] != '_' and n[-1] != '_']
        for property_name in property_names:
            self.__dict__[property_name[1:]] = read_only_property(lambda self: self.__dict__[property_name])


    def _get_curve_value(self, min_stat, max_stat, curve, max_level, level):
        return round(min_stat + (max_stat - min_stat) * ((level - 1) / (max_level - 1)) ** curve)

    def _get_stat_at_level(self, min_stat, max_stat, curve, level):
        if type(level) != int:
            raise ValueError('level must be an int')
        if level < 1:
            raise ValueError('level must be greater than or equal to 1')
        if level <= self._max_level:
            return self._get_curve_value(min_stat, max_stat, curve, self._max_level, level)
        if self._max_level == 99 and self.limitbreakable:
            if level <= 110:
                return max_stat * (1 + self._limitbreak_stat_increase * ((level - 99) / 11))
            raise ValueError('level must be less than or equal to 110')
        raise ValueError('level must be less than or equal to 99')

    def get_hp_at_level(self, level):
        return self._get_stat_at_level(self._hp_minimum, self._hp_maximum, self._hp_curve, level)

    def get_atk_at_level(self, level):
        return self._get_stat_at_level(self._atk_minimum, self._atk_maximum, self._atk_curve, level)

    def get_rcv_at_level(self, level):
        return self._get_stat_at_level(self._rcv_minimum, self._rcv_maximum, self._rcv_curve, level)

    def to_json(self, localization_region=None) -> dict:
        card_json = {
            'id': self._id,
            'name': self._name,
            'attribute': self._attribute.value,
            'subattribute': self._subattribute.value,
            'types': [t.value for t in self._types],
            'rarity': self._rarity,
            'cost': self._cost,
            'max_level': self._max_level,
            'feed_experience_per_level': self._feed_experience_per_level,
            'released': self._released,
            'sell_value_coin_per_level': self._sell_value_coin_per_level,
            'hp_minimum': self._hp_minimum,
            'hp_maximum': self._hp_maximum,
            'hp_curve': self._hp_curve,
            'atk_minimum': self._atk_minimum,
            'atk_maximum': self._atk_maximum,
            'atk_curve': self._atk_curve,
            'rcv_minimum': self._rcv_minimum,
            'rcv_maximum': self._rcv_maximum,
            'rcv_curve': self._rcv_curve,
            'max_experience': self._max_experience,
            'experience_curve': self._experience_curve,
            'active_skill_id': self._active_skill_id,
            'leader_skill_id': self._leader_skill_id,
            'awakenings': [a.value for a in self._awakenings],
            'super_awakenings': [a.value for a in self._super_awakenings],
            'base_evo_id': self._base_evo_id,
            'group': self._group,
            'sell_value_mp': self._sell_value_mp,
            'latent_on_fuse': self._latent_on_fuse.value,
            'collab': self._collab,
            'inheritable': self._inheritable,
            'furigana': self._furigana,
            'limitbreakable': self.limitbreakable,
            'limitbreak_stat_increase': self._limitbreak_stat_increase,
        }
        return card_json

    # The following code is terrible
    # TODO find better solution

    @read_only_property
    def region(self):
        return self._region

    @read_only_property
    def id(self):
        return self._id
        
    @read_only_property
    def attribute(self):
        return self._attribute
        
    @read_only_property
    def subattribute(self):
        return self._subattribute
        
    @read_only_property
    def types(self):
        return self._types
        
    @read_only_property
    def rarity(self):
        return self._rarity
        
    @read_only_property
    def cost(self):
        return self._cost
        
    @read_only_property
    def size(self):
        return self._size
        
    @read_only_property
    def max_level(self):
        return self._max_level
        
    @read_only_property
    def feed_experience_per_level(self):
        return self._feed_experience_per_level
        
    @read_only_property
    def released(self):
        return self._released
        
    @read_only_property
    def sell_value_coin_per_level(self):
        return self._sell_value_coin_per_level
        
    @read_only_property
    def hp_minimum(self):
        return self._hp_minimum
        
    @read_only_property
    def hp_maximum(self):
        return self._hp_maximum
        
    @read_only_property
    def hp_curve(self):
        return self._hp_curve
        
    @read_only_property
    def atk_minimum(self):
        return self._atk_minimum
        
    @read_only_property
    def atk_maximum(self):
        return self._atk_maximum
        
    @read_only_property
    def atk_curve(self):
        return self._atk_curve
        
    @read_only_property
    def rcv_minimum(self):
        return self._rcv_minimum
        
    @read_only_property
    def rcv_maximum(self):
        return self._rcv_maximum
        
    @read_only_property
    def rcv_curve(self):
        return self._rcv_curve
        
    @read_only_property
    def max_experience(self):
        return self._max_experience
        
    @read_only_property
    def experience_curve(self):
        return self._experience_curve
        
    @read_only_property
    def leader_skill_id(self):
        return self._leader_skill_id
        
    @read_only_property
    def active_skill_id(self):
        return self._active_skill_id
        
    @read_only_property
    def awakenings(self):
        return self._awakenings
        
    @read_only_property
    def super_awakenings(self):
        return self._super_awakenings
        
    @read_only_property
    def base_evo_id(self):
        return self._base_evo_id
        
    @read_only_property
    def group(self):
        return self._group
        
    @read_only_property
    def sell_value_mp(self):
        return self._sell_value_mp
        
    @read_only_property
    def latent_on_fuse(self):
        return self._latent_on_fuse
        
    @read_only_property
    def collab(self):
        return self._collab
        
    @read_only_property
    def inheritable(self):
        return self._inheritable
        
    @read_only_property
    def furigana(self):
        return self._furigana
        
    @read_only_property
    def limitbreakable(self):
        return self._limitbreak_stat_increase > 0.0
        
    @read_only_property
    def limitbreak_stat_increase(self):
        return self._limitbreak_stat_increase

    @read_only_property
    def voice(self):
        return self._voice

    @read_only_property
    def orb_skin(self):
        return self._orb_skin
            