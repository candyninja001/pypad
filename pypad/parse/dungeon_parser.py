from .json_parser import JsonParser
from common import gungho_csv, binary_to_list

def _category_convert(category_number):
    if category_number == '0':
        return 'normal'
    if category_number == '1':
        return 'special'
    if category_number == '2':
        return 'technical'
    if category_number == '3':
        return 'bonus'
    if category_number == '4':
        return 'tournament'
    if category_number == '5':
        return '2-player'
    if category_number == '6':
        return 'unknown_6'
    if category_number == '7':
        return '3-player'
    return 'unknown_'+str(category_number)

def _tab_convert(tab_number):
    if tab_number == '':
        return ''
    if tab_number == '0':
        return 'special'
    if tab_number == '1':
        return '1'
    if tab_number == '2':
        return '2'
    if tab_number == '3':
        return '3'
    if tab_number == '101':
        return 'descended'
    if tab_number == '102':
        return 'collab'
    if tab_number == '103':
        return 'gift'
    if tab_number == '202':
        return 'tutorial'
    if tab_number == '1001':
        return 'EX 1'
    if tab_number == '1002':
        return 'EX 2'
    if tab_number == '2000':
        return 'arena'
    return 'unknown_'+str(tab_number)


class DungeonParser(JsonParser):
    _dungeon_tags = {
        '1': 'solo',
        'Q': 'quest',
        'C': 'collab',
        'G': 'guerrilla'
    }

    def parsable(self, raw_data: dict) -> bool:
        return 'dungeons' in raw_data

    def version(self) -> int:
        return 6

    def parse(self, raw_data: dict) -> dict:
        self._clear_reports()

        parsed_json = {}
        parsed_json['dungeons'] = {}

        raw_csv = gungho_csv(raw_data['dungeons'])
        current_dungeon_id = 0
        for line in raw_csv:
            line_type = line[0][0:1]
            line_id = line[0][2:]

            if line_type == 'c':
                pass # ckey
            
            elif line_type == 'd':
                dungeon = {}
                dungeon['floors'] = {}
                dungeon['id'] = int(line_id)
                dungeon['name'] = line[1]
                dungeon['tag'] = 'none'
                dungeon['color'] = '000000'
                
                if len(dungeon['name']) > 3 and dungeon['name'][0] == '#' and dungeon['name'][2] == '#':
                    tag_letter = dungeon['name'][1]
                    dungeon['name'] = dungeon['name'][3:]
                    if tag_letter in DungeonParser._dungeon_tags:
                        dungeon['tag'] = DungeonParser._dungeon_tags[tag_letter]
                    else:
                        dungeon['tag'] = tag_letter
                if len(dungeon['name']) > 8 and dungeon['name'][0] == '$' and dungeon['name'][7] == '$':
                    dungeon['color'] = dungeon['name'][1:7]
                    dungeon['name'] = dungeon['name'][8:]
                    
                dungeon['background'] = int(line[2])
                dungeon['category'] = _category_convert(line[3])
                dungeon['sub_category'] = int(line[4])
                dungeon['sort_order'] = int(line[5])
                dungeon['tab'] = _tab_convert(line[6])
                dungeon['sub_tab'] = line[7]
                dungeon['monster_art'] = int(line[8]) if len(line) >= 9 else 0
                
                parsed_json['dungeons'][dungeon['id']] = dungeon
                current_dungeon_id = dungeon['id']
        
            elif line_type == 'f':
                floor = {}
                floor['id'] = int(line_id)
                floor['name'] = line[1]
                floor['battles'] = int(line[2])
                floor['type'] = int(line[3])
                floor['stamina'] = int(line[4])
                # unknown = int(line[5])
                # unknown = int(line[6])
                # unknown = int(line[7])
                monster = int(line[8])
                next_start_index = 9
                floor['monsters'] = []
                while monster != 0:
                    floor['monsters'].append(monster)
                    monster = int(line[next_start_index])
                    next_start_index += 1

                floor['unlock_requirement'] = 0 # 0 - 1    # the dungeon that must be cleared for this dungeon to appear, if id matches the dungeon, all floors below must be cleared, eg arena
                #floor['???'] = 0               # 1 - 2
                #floor['???'] = 0               # 2 - 4
                floor['s_rank_score'] = 0       # 3 - 8
                #floor['???'] = 0               # 4 - 16
                floor['restrictions'] = []      # 5 - 32
                floor['modifiers'] = []         # 6 - 64

                

                floor['bitmap_int'] = int(line[next_start_index])
                bitmap = binary_to_list(int(line[next_start_index]))
                floor['bitmap'] = bitmap
                floor['bitmap_args'] = [line[next_start_index + i] for i in range(len(bitmap), 0, -1)]
                next_start_index += 1

                if any(b not in {0,2,3,4,5,6} for b in bitmap):
                    self._report(f'[{current_dungeon_id}:{floor["id"]}] Unexpected bitmap type')
                    
                if 0 in bitmap:
                    floor['unlock_requirement'] = {'dungeon': int(line[next_start_index]), 'floor': int(line[next_start_index + 1])}
                    next_start_index += 2
                else:
                    floor['unlock_requirement'] = {'dungeon': 0, 'floor': 0}
                    
                if 2 in bitmap:
                    next_start_index += 1
                else:
                    pass
                
                if 3 in bitmap:
                    floor['s_rank_score'] = int(line[next_start_index])
                    next_start_index += 1
                else:
                    floor['s_rank_score'] = 0
                    
                if 4 in bitmap:
                    next_start_index += 1
                else:
                    pass

                floor['modifiers'] = []
                if 6 in bitmap:
                    modifier_list = [m.split(':') for m in line[next_start_index].split('|')]
                    modifiers = {m[0]:(m[1] if len(m) > 1 else True) for m in modifier_list}
                    for name,value in modifiers.items():
                        if name == '7*6':
                            floor['modifiers'].append({'type': 'large_board', 'args': {}})
                        elif name == '5*4':
                            floor['modifiers'].append({'type': 'small_board', 'args': {}})
                        elif name == 'hp':
                            floor['modifiers'].append({'type': 'enemy_hp_multiplier', 'args': {'multiplier': int(value)/10000}})
                        elif name == 'at':
                            floor['modifiers'].append({'type': 'enemy_attack_multiplier', 'args': {'multiplier': int(value)/10000}})
                        elif name == 'df':
                            floor['modifiers'].append({'type': 'enemy_defense_multiplier', 'args': {'multiplier': int(value)/10000}})
                        elif name == 'battr':
                            args = value.split(';')
                            floor['modifiers'].append({'type': 'attribute_bonus', 'args': {'attributes': binary_to_list(int(args[0])), 'hp_multiplier': int(args[1])/10000, 'atk_multiplier': int(args[2])/10000, 'rcv_multiplier': int(args[3])/10000}})
                        elif name.startswith('dmsg'):
                            i = int(name[4:])
                            floor['modifiers'].append({'type': f'd_message_{i}', 'args': {'text': value}})
                        elif name == 'dg':
                            floor['modifiers'].append({'type': 'dungeon_environment', 'args': {'id': int(value)}}) # best guess, the appearance of the dungeon, eg normals are a dungeon but arena is the arena background, seems to differentiate different designs per floor vs per dungeon
                        elif name == 'btype':
                            args = value.split(';')
                            floor['modifiers'].append({'type': 'type_bonus', 'args': {'types': binary_to_list(int(args[0])), 'hp_multiplier': int(args[1])/10000, 'atk_multiplier': int(args[2])/10000, 'rcv_multiplier': int(args[3])/10000}})
                        elif name.startswith('smsg'):
                            i = int(name[4:])
                            floor['modifiers'].append({'type': f's_message_{i}', 'args': {'text': value}})
                        elif name.startswith('fc'):
                            i = int(name[2:])
                            values = [int(x) if x != '' else 0 for x in value.split(';')]
                            default_stats = [99,0,0,0,99,99] # best guess, [level,+hp,+atk,+rcv,awakenings,skill_level]
                            stats = [values[1 + i] if i < len(values) - 1 else default_stats[i] for i in range(len(default_stats))]
                            floor['modifiers'].append({'type': f'fixed_card_{i}', 'args': {'id': values[0], 'level': stats[0], 'plus_hp': stats[1], 'plus_atk': stats[2], 'plus_rcv': stats[3], 'awakenings': stats[4], 'skill_level': stats[5]}})
                        elif name == 'brare':
                            args = value.split(';')
                            floor['modifiers'].append({'type': 'rarity_bonus', 'args': {'rarities': binary_to_list(int(args[0])), 'hp_multiplier': int(args[1])/10000, 'atk_multiplier': int(args[2])/10000, 'rcv_multiplier': int(args[3])/10000}})
                        elif name == 'ndf':
                            floor['modifiers'].append({'type': 'no_skyfall', 'args': {}})
                        elif name == 'ft':
                            floor['modifiers'].append({'type': 'fixed_time', 'args': {'time': int(value)/10}})
                        elif name == 'ta': # TODO verify
                            floor['modifiers'].append({'type': 'time_limit', 'args': {'time': int(value)}})
                        elif name == 'hp_fix':
                            floor['modifiers'].append({'type': 'fixed_hp', 'args': {'hp': int(value)}})
                        else:
                            # TODO decode the other meanings
                            self._report_dev(f'[{current_dungeon_id}:{floor["id"]}] Unexpected modifier: {name}:{value}')
                    next_start_index += 1

                floor['restrictions'] = []
                if 5 in bitmap:
                    args = [int(x) for x in line[next_start_index:]]
                    if args[0] == 2:
                        floor['restrictions'].append({'type': 'max_cost', 'args': {'cost': args[1]}})
                    elif args[0] == 4:
                        floor['restrictions'].append({'type': 'max_rarity', 'args': {'rarity': args[1]}})
                    elif args[0] == 7:
                        floor['restrictions'].append({'type': 'type_restriction', 'args': {'type': args[1]}})
                    elif args[0] == 9:
                        floor['restrictions'].append({'type': 'attributes_required', 'args': {'attributes': [a-1 for a in args[1:]]}})
                    elif args[0] == 10:
                        floor['restrictions'].append({'type': 'no_dupes', 'args': {}}) # sometimes has args[1] == 4, unsure of meaning
                    elif args[0] == 11:
                        floor['restrictions'].append({'type': 'roguelike', 'args': {'arg_'+str(i):args[i] for i in range(1, len(args))}}) # decode later, guessing they are multipliers of exp values
                    elif args[0] == 13:
                        floor['restrictions'].append({'type': 'monster_required', 'args': {'id': args[1]}})
                    elif args[0] == 14:
                        floor['restrictions'].append({'type': 'max_team_size', 'args': {'count': args[1]}})
                    else:
                        self._report_dev(f'[{current_dungeon_id}:{floor["id"]}] Unexpected restriction type: {args[0]}')
                
                floor['line'] = line
                parsed_json['dungeons'][current_dungeon_id]['floors'][floor['id']] = floor

        return parsed_json

        