from .region import Region
from .attack_attribute import AttackAttribute
from .monster_type import MonsterType
from .collab import Collab


class EnemySkillInstance:
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
        # 13 - 24 Card
        self.skill_up_skill_id = raw_card[25]
        # 26 Card

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
            self.skill_set._register(EnemySkillInstance(raw_card[58 + i*3], raw_card[59 + i*3], raw_card[60 + i*3]))
        
        i = 3 * enemy_skill_count

        awakening_count = raw_card[i+58]
        j = i + awakening_count

        # 58 - 61 Card
        
        self.types.append(MonsterType(raw_card[j+62]))
        self.types = tuple(t for t in self.types if t != MonsterType.NONE)

        # 63 - 64 Card

        self.collab = Collab(raw_card[j+65])


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
            'skill_up_skill_id': self.skill_up_skill_id,
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
            'collab': self.collab,
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

    def __len__(self):
        return len(self._enemies)

    def variants_of(self, monster_id):
        variants = []
        while monster_id in self._enemies:
            variants.append(self._enemies[monster_id])
            monster_id += 100000
        return variants

    def to_json(self):
        return {str(m_id):json for m_id,json in sorted((m_id,card.to_json()) for m_id,card in self._enemies.items())}