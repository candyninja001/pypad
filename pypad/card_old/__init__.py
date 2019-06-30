from ..region import Region
from ..attack_attribute import AttackAttribute
from ..monster_type import MonsterType
from ..awakening import Awakening
from ..latent_awakening import LatentAwakening

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
        self.collab = raw_card[j+65] # TODO create a Collab class or enum
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
            'collab': self.collab,
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

    def _register(self, card: CardData):
        # only add cards, not alternate enemies
        if card.id != 0 and card.id < 100000:
            self._cards[card.id] = card

    def __getitem__(self, key) -> CardData:
        return self._cards[key]

    def __contains__(self, key) -> bool:
        return key in self._cards

    def __iter__(self):
        return iter(self._cards.values())

    def to_json(self) -> dict:
        return {str(m_id):json for m_id,json in sorted((m_id,card.to_json()) for m_id,card in self._cards.items())}


class BoxCard:
    def __init__(self, raw_box_card):
        self.chr_id = raw_box_card[0]
        self.experience = raw_box_card[1]
        self.level = raw_box_card[2]
        self.skill_level = raw_box_card[3]
        self._fuse_count = raw_box_card[4] # TODO verify
        self.monster_id = raw_box_card[5]
        self.plus_hp = raw_box_card[6]
        self.plus_atk = raw_box_card[7]
        self.plus_rcv = raw_box_card[8]
        self.awakenings = raw_box_card[9]
        self._latent_awakenings = raw_box_card[10] # TODO convert from binary to LatentAwakening
        self.inherit_chr_id = raw_box_card[11]
        self.super_awakening_roll_progress = raw_box_card[12]
        self.super_awakening = Awakening(raw_box_card[13])
        # self._unknown_14 = raw_box_card[14]


class MonsterBox:
    def __init__(self):
        self._cards = {}
    
    def _register(self, raw_monster):
        # dont register materials
        if raw_monster[0] < 0xFFFF0000:
            self._cards[raw_monster[0]] = BoxCard(raw_monster)

    def __getitem__(self, chr_id):
        return self._cards[chr_id]


class MaterialsBox:
    def __init__(self):
        self._materials = {}

    def _register(self, raw_material):
        # only register materials
        if raw_material[0] > 0xFFFF0000:
            self._materials[raw_material[5]] = raw_material[1]

    def __contains__(self, monster_id):
        return self.__getitem__(monster_id) > 0
    
    def __getitem__(self, monster_id):
        if monster_id not in self._materials:
            return 0
        return self._materials[monster_id]


class EnemySkill:
    def __init__(self, enemy_skill_id, ai, rnd):
        self.enemy_skill_id = enemy_skill_id
        self.ai = ai
        self.rnd = rnd

    def to_json(self):
        return {
            'enemy_skill_id': self.enemy_skill_id,
            'ai': self.ai,
            'rnd': self.rnd,
        }


class EnemySkillSet:
    def __init__(self):
        self._skills = []

    def _register(self, enemy_skill):
        self._skills.append(enemy_skill)

    def __getitem__(self, key):
        self._skills[key]

    def to_json(self):
        return {str(i): self._skills[i].to_json() for i in range(len(self._skills))}


class EnemyData:
    def __init__(self, raw_card, region=Region.NA):
        self.id = raw_card[0]
        self.name = raw_card[1]
        self.attribute = AttackAttribute(raw_card[2])
        self.subattribute = AttackAttribute(raw_card[3])
        # 4 Evolution
        self.types = [MonsterType(raw_card[5])]
        self.types.append(MonsterType(raw_card[6]))
        # 7 - 8 Card
        self.size = raw_card[9] # TODO turn size into an enum
        # 10 - 11 Card
        self.released = raw_card[12] == 100

        # 13 - 26 Card

        self.turn_timer_normal = raw_card[27]
        self.hp_at_lv_1 = raw_card[28]
        self.hp_at_lv_10 = raw_card[29]
        self.hp_curve = raw_card[30]
        self.atk_at_lv_1 = raw_card[31]
        self.atk_at_lv_10 = raw_card[32]
        self.atk_curve = raw_card[33]
        self.def_at_lv_1 = raw_card[34]
        self.def_at_lv_10 = raw_card[35]
        self.def_curve = raw_card[36]
        self.max_level = raw_card[37]
        self.coins_at_lv_2 = raw_card[38]
        self.experience_at_lv_2 = raw_card[39]

        # 40 - 50 Evolution

        self.turn_timer_technical = raw_card[51]
        self._unknown_52 = raw_card[52]
        self._unknown_53 = raw_card[53]
        self._unknown_54 = raw_card[54]
        self._unknown_55 = raw_card[55]
        self._unknown_56 = raw_card[56]

        enemy_skill_count = raw_card[57]
        self.skill_set = EnemySkillSet()
        for i in range(enemy_skill_count):
            self.skill_set._register(EnemySkill(raw_card[58 + i*3], raw_card[59 + i*3], raw_card[60 + i*3]))
        
        i = 3 * enemy_skill_count

        awakening_count = raw_card[i+58]
        j = i + awakening_count

        # 58 - 61 Card
        
        self.types.append(MonsterType(raw_card[j+62]))
        self.types = tuple(t for t in self.types if t != MonsterType.NONE)


    def _get_curve_value(self, stat_at_lv_1, stat_at_lv_10, level):
        return round(stat_at_lv_1 + (stat_at_lv_10 - stat_at_lv_1) * (level - 1) / 9)

    def _get_stat_at_level(self, stat_at_lv_1, stat_at_lv_10, level):
        if type(level) != int:
            raise ValueError('level must be an int')
        if level < 1:
            raise ValueError('level must be greater than or equal to 1')
        level = min(level, self.max_level)
        return self._get_curve_value(stat_at_lv_1, stat_at_lv_10, level)

    def get_hp_at_level(self, level):
        return self._get_stat_at_level(self.hp_at_lv_1, self.hp_at_lv_10, level)

    def get_atk_at_level(self, level):
        return self._get_stat_at_level(self.atk_at_lv_1, self.atk_at_lv_10, level)

    def get_def_at_level(self, level):
        return self._get_stat_at_level(self.def_at_lv_1, self.def_at_lv_10, level)

    def get_coins_at_level(self, level):
        return round(self.coins_at_lv_2 * level / 2)

    def get_experience_at_level(self, level):
        return round(self.experience_at_lv_2 * level / 2)

    def to_json(self) -> dict:
        return {
            'id': self.id,
            'name': self.name,
            'attribute': self.attribute.value,
            'subattribute': self.subattribute.value,
            'types': [t.value for t in self.types],
            'width': self.size,
            'released': self.released,
            'turn_timer_normal': self.turn_timer_normal,
            'hp_at_lv_1': self.hp_at_lv_1,
            'hp_at_lv_10': self.hp_at_lv_10,
            'hp_curve': self.hp_curve,
            'atk_at_lv_1': self.atk_at_lv_1,
            'atk_at_lv_10': self.atk_at_lv_10,
            'atk_curve': self.atk_curve,
            'def_at_lv_1': self.def_at_lv_1,
            'def_at_lv_10': self.def_at_lv_10,
            'def_curve': self.def_curve,
            'max_level': self.max_level,
            'coins_at_lv_2': self.coins_at_lv_2,
            'experience_at_lv_2': self.experience_at_lv_2,
            'turn_timer_technical': self.turn_timer_technical,
            '_unknown_52': self._unknown_52,
            '_unknown_53': self._unknown_53,
            '_unknown_54': self._unknown_54,
            '_unknown_55': self._unknown_55,
            '_unknown_56': self._unknown_56,
            'skill_set': self.skill_set.to_json(),
        }


class EnemyMonsterBook:
    def __init__(self):
        self._enemies = {}

    def _register(self, enemy):
        if enemy.id != 0:
            self._enemies[enemy.id] = enemy

    def __getitem__(self, monster_id):
        return self._enemies[monster_id]

    def __contains__(self, monster_id):
        return monster_id in self._enemies

    def __iter__(self):
        return iter(self._enemies.values())

    def variants_of(self, monster_id):
        variants = []
        while monster_id in self._enemies:
            variants.append(self._enemies[monster_id])
            monster_id += 100000
        return variants

    def to_json(self):
        return {str(m_id):json for m_id,json in sorted((m_id,card.to_json()) for m_id,card in self._enemies.items())}