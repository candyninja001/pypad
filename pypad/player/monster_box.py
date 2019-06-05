from ..awakening import Awakening
from ..region import Region   

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

    def __iter__(self):
        return iter(self._cards.values())

    def __len__(self):
        return len(self._cards)


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

    def __len__(self):
        return len(self._materials)