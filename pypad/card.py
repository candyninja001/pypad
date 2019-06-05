from .region import Region
from .attack_attribute import AttackAttribute
from .monster_type import MonsterType
from .awakening import Awakening
from .latent_awakening import LatentAwakening
from .collab import Collab
from collections import defaultdict

class CardData:
    def __init__(self, raw_card, region=Region.NA):
        self.id = raw_card[0]
        self.name = raw_card[1]
        self.attribute = AttackAttribute(raw_card[2])
        self.subattribute = AttackAttribute(raw_card[3])
        # 4 is_ultimate in Evolution
        self.types = [MonsterType(raw_card[5])]
        self.types.append(MonsterType(raw_card[6]))
        self.rarity = raw_card[7]
        self.cost = raw_card[8]
        # 9 width of enemy
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
        self.collab = Collab(raw_card[j+65])
        self.inheritable = raw_card[j+66] = 3
        self.furigana = raw_card[j+67]
        self.limitbreak_stat_increase = raw_card[j+68] / 100
        self.voice = raw_card[j+69] # TODO create a Voice class or enum
        self.orb_skin = raw_card[j+70] # TODO create an OrbSkin class or enum


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
                return round(max_stat * (1 + self.limitbreak_stat_increase * ((level - 99) / 11)))
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
            'collab': self.collab.value,
            'inheritable': self.inheritable,
            'furigana': self.furigana,
            'limitbreakable': self.limitbreakable,
            'limitbreak_stat_increase': self.limitbreak_stat_increase,
            'voice_id': self.voice,
            'orb_skin_unlock': self.orb_skin,
        }

    @property
    def limitbreakable(self):
        return self.limitbreak_stat_increase > 0.0


class MonsterBook:
    def __init__(self):
        self._cards = {}
        self._active_skill_map = defaultdict(set)
        self._leader_skill_map = defaultdict(set)

    def _register(self, card: CardData):
        # only add cards, not alternate enemies
        if card.id != 0 and card.id < 100000 and card.released:
            self._cards[card.id] = card
            if card.active_skill_id != 0:
                self._active_skill_map[card.active_skill_id].add(card.id)
            if card.leader_skill_id != 0:
                self._leader_skill_map[card.leader_skill_id].add(card.id)

    def __getitem__(self, key) -> CardData:
        return self._cards[key]

    def __contains__(self, key) -> bool:
        return key in self._cards

    def __iter__(self):
        return iter(self._cards.values())

    def __len__(self):
        return len(self._cards)

    def to_json(self) -> dict:
        return {str(m_id):json for m_id,json in sorted((m_id,card.to_json()) for m_id,card in self._cards.items())}

    def cards_with_active_skill_id(self, active_skill_id: int) -> set:
        if active_skill_id not in self._active_skill_map:
            return set()
        return {self._cards[m_id] for m_id in self._active_skill_map[active_skill_id]}

    def cards_with_leader_skill_id(self, leader_skill_id: int) -> set:
        if leader_skill_id not in self._leader_skill_map:
            return set()
        return {self._cards[m_id] for m_id in self._leader_skill_map[leader_skill_id]}