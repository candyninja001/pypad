from .json_parser import JsonParser
from collections import defaultdict

class CardParser(JsonParser):
    def parsable(self, raw_data: dict) -> bool:
        return 'skill' in raw_data

    def version(self) -> int:
        return 1250

    def parse(self, raw_data: dict) -> dict:
        self._clear_reports()

        parsed_json = {}
        parsed_json['version'] = raw_data['v']
        parsed_json['cards'] = {}
        parsed_json['enemies'] = {}
        parsed_json['evolutions'] = defaultdict(list)
        for raw_card in raw_data['card']:
            parsed_card = {}
            parsed_card['id'] = raw_card[0]
            parsed_card['name'] = raw_card[1]
            parsed_card['attribute'] = raw_card[2]
            parsed_card['subattribute'] = raw_card[3]
            parsed_card['types'] = [raw_card[t] for t in [5,6] if raw_card[t] != -1]
            parsed_card['rarity'] = raw_card[7]
            parsed_card['cost'] = raw_card[8]
            # 9 unknown
            parsed_card['max_level'] = raw_card[10]
            parsed_card['feed_experience'] = raw_card[11] / 4 # per level
            parsed_card['released'] = raw_card[12] == 100
            parsed_card['sell_value_coin'] = raw_card[13] / 10 # per level
            parsed_card['hp_minimum'] = raw_card[14]
            parsed_card['hp_maximum'] = raw_card[15]
            parsed_card['hp_curve'] = raw_card[16]
            parsed_card['atk_minimum'] = raw_card[17]
            parsed_card['atk_maximum'] = raw_card[18]
            parsed_card['atk_curve'] = raw_card[19]
            parsed_card['rcv_minimum'] = raw_card[20]
            parsed_card['rcv_maximum'] = raw_card[21]
            parsed_card['rcv_curve'] = raw_card[22]
            parsed_card['max_experience'] = raw_card[23]
            parsed_card['experience_curve'] = raw_card[24]
            parsed_card['active_skill_id'] = raw_card[25]
            parsed_card['leader_skill_id'] = raw_card[26]
            
            parsed_enemy = {}
            parsed_enemy['id'] = parsed_card['id']
            parsed_enemy['turn_timer_normal'] = raw_card[27]
            parsed_enemy['hp_at_lv_1'] = raw_card[28]
            parsed_enemy['hp_at_lv_10'] = raw_card[29]
            parsed_enemy['hp_curve'] = raw_card[30]
            parsed_enemy['atk_at_lv_1'] = raw_card[31]
            parsed_enemy['atk_at_lv_10'] = raw_card[32]
            parsed_enemy['atk_curve'] = raw_card[33]
            parsed_enemy['def_at_lv_1'] = raw_card[34]
            parsed_enemy['def_at_lv_10'] = raw_card[35]
            parsed_enemy['def_curve'] = raw_card[36]
            parsed_enemy['max_level'] = raw_card[37]
            parsed_enemy['coins_at_lv_2'] = raw_card[38]
            parsed_enemy['experience_at_lv_2'] = raw_card[39]
            
            if raw_card[40] != 0:
                evo = {}
                evo['base'] = raw_card[40]
                evo['materials'] = [raw_card[t] for t in range(41,46) if raw_card[t] != 0]
                evo['is_ultimate'] = raw_card[4] == 1
                evo['result'] = parsed_card['id']
                evo['devo_materials'] = [raw_card[t] for t in range(46,51) if raw_card[t] != 0]
                parsed_json['evolutions'][evo['base']].append(evo)
            
            parsed_enemy['turn_timer_technical'] = raw_card[51]
            # 52 unknown
            # 53 unknown
            # 54 unknown
            # 55 unknown
            if raw_card[56] != 0: self._report_dev(f"({parsed_card['id']}) Non-zero u56: {raw_card[56]}")
            
            enemy_skill_count = raw_card[57]
            parsed_enemy['skills'] = []
            for i in range(enemy_skill_count):
                enemy_skill = {}
                enemy_skill['enemy_skill_id'] = raw_card[58 + 3 * i]
                enemy_skill['ai'] = raw_card[59 + 3 * i]
                enemy_skill['rnd'] = raw_card[60 + 3 * i]
                parsed_enemy['skills'].append(enemy_skill)
            
            index_shift_1 = 58 + 3 * enemy_skill_count
            awakening_count = raw_card[index_shift_1]
            parsed_card['awakenings'] = [raw_card[a + index_shift_1 + 1] for a in range(awakening_count)]
            
            index_shift_2 = index_shift_1 + awakening_count + 1
            parsed_card['superawakenings'] = [int(a) for a in raw_card[index_shift_2].split(',') if a != '']
            parsed_card['base_evo_id'] = raw_card[index_shift_2 + 1]
            parsed_card['group'] = raw_card[index_shift_2 + 2]
            parsed_card['types'].extend([raw_card[index_shift_2 + 3]] if -1 != -1 else []) # add type 3
            parsed_card['sell_value_mp'] = raw_card[index_shift_2 + 4]
            parsed_card['latent_on_fuse'] = raw_card[index_shift_2 + 5] # which latent awakening is granted upon fusing this card away
            parsed_card['collab'] = raw_card[index_shift_2 + 6] # collab id, also includes dbdc as a special collab id
            parsed_card['inheritable'] = raw_card[index_shift_2 + 7] == 3
            parsed_card['furigana'] = raw_card[index_shift_2 + 8]
            parsed_card['limitbreakable'] = raw_card[index_shift_2 + 9] > 0
            parsed_card['limitbreak_stat_increase'] = raw_card[index_shift_2 + 9] / 100 # percentage increase
            parsed_json['cards'][parsed_card['id']] = parsed_card
            parsed_json['enemies'][parsed_enemy['id']] = parsed_enemy
        return parsed_json
